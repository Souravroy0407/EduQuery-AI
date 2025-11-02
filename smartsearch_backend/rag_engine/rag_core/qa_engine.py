"""
RAG QA engine:
- retrieves context via vector_store.query_faiss
- sends prompt + context to Ollama (local) for generation
- automatic fallback to OpenRouter if Ollama fails or times out
"""

import os
import json
import requests
from typing import List
from langchain_core.documents import Document

# === SETTINGS ===
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")  # light and fast
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")  # optional key for fallback
OPENROUTER_MODEL = "tngtech/deepseek-r1t2-chimera:free"

PROMPT_TEMPLATE = """You are EduQuery AI — a helpful assistant for students.
Use the provided context (accurately cite sources from the context) to answer the question concisely.

Context:
{context}

Question:
{question}

Answer clearly and student-friendly. If the answer is not found in the context, say so politely and suggest next steps.
"""

# === BUILD CONTEXT ===
def _build_context_text(docs: List[Document]) -> str:
    parts = []
    for i, d in enumerate(docs):
        meta = getattr(d, "metadata", {}) or {}
        src = meta.get("source", f"chunk_{i}")
        parts.append(f"[{src}] {d.page_content}")
    return "\n\n".join(parts)


# === OLLAMA GENERATION ===
def generate_with_ollama(prompt: str, max_tokens: int = 512) -> str:
    """Call local Ollama model via HTTP API"""
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "options": {"temperature": 0.7, "num_predict": max_tokens},
        "stream": False,
    }

    try:
        print(f"🧠 Sending prompt to Ollama model='{OLLAMA_MODEL}' ...")
        resp = requests.post(url, json=payload, timeout=60)  # ⏱️ increased timeout
        resp.raise_for_status()
        data = resp.json()

        # handle different Ollama JSON responses
        if isinstance(data, dict):
            for key in ("response", "text", "completion", "content", "output"):
                if key in data and isinstance(data[key], str):
                    return data[key].strip()
        return json.dumps(data)
    except Exception as e:
        print(f"⚠️ Ollama failed: {e}")
        # fallback to OpenRouter if key provided
        if OPENROUTER_KEY:
            print("🌐 Falling back to OpenRouter...")
            return generate_with_openrouter(prompt, max_tokens)
        return f"Error calling Ollama: {e}"


# === OPENROUTER FALLBACK ===
def generate_with_openrouter(prompt: str, max_tokens: int = 512) -> str:
    """Call OpenRouter (DeepSeek) fallback model"""
    if not OPENROUTER_KEY:
        return "OpenRouter API key not configured."
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error calling OpenRouter: {e}"


# === MAIN RAG PIPELINE ===
def answer_question(question: str, retriever_fn, k: int = 4) -> dict:
    """Main RAG function"""
    print(f"🔍 Retrieving top-{k} relevant chunks...")
    docs = retriever_fn(question, k=k)
    context_text = _build_context_text(docs)
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=question)
    answer = generate_with_ollama(prompt)
    sources = [d.metadata for d in docs]
    print("✅ Answer generation complete.")
    return {"answer": answer, "sources": sources, "context": context_text}
