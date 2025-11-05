#  backend/rag_engine/rag_core/qa_engine.py

"""
RAG QA engine:
- retrieves context via vector_store.query_faiss
- selects model dynamically (phi3 fast / llama3 deep)
- runs Ollama (local) and OpenRouter (global) in parallel
- returns whichever responds first for best speed + reliability
"""

import os
import json
import requests
import psutil
import concurrent.futures
from typing import List
from langchain_core.documents import Document

# === SETTINGS ===
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")  # optional key for fallback
OPENROUTER_MODEL = "tngtech/deepseek-r1t2-chimera:free"

PROMPT_TEMPLATE = """You are EduQuery AI — a helpful assistant for students.
Use the provided context (accurately cite sources from the context) to answer the question concisely.

Context:
{context}

Question:
{question}

If the context does not contain relevant information, do NOT guess or invent details.
Instead, reply politely:
"I couldn’t find relevant information in your uploaded materials.
Please upload a related PDF or ask a different question."

Answer clearly and in a student-friendly tone.
"""

# === BUILD CONTEXT ===
def _build_context_text(docs: List[Document]) -> str:
    if not docs:
        return ""
    parts = []
    for i, d in enumerate(docs):
        meta = getattr(d, "metadata", {}) or {}
        src = meta.get("source", f"chunk_{i}")
        parts.append(f"[{src}] {d.page_content}")
    return "\n\n".join(parts)


# === MODEL CHOICE BASED ON MEMORY ===
def choose_model_based_on_memory() -> str:
    """Decide between llama3 (deep) and phi3 (fast) depending on available memory."""
    available_gb = psutil.virtual_memory().available / (1024 ** 3)
    if available_gb < 6:
        print(f"⚡ Low memory ({available_gb:.2f} GB available) → Using phi3 for speed.")
        return "phi3"
    else:
        print(f"🧠 Sufficient memory ({available_gb:.2f} GB) → Using llama3 for depth.")
        return "llama3"


# === OLLAMA GENERATION (LOCAL) ===
def generate_with_ollama(prompt: str, max_tokens: int = 512) -> str:
    """Call local Ollama model via HTTP API"""
    model_name = choose_model_based_on_memory()
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "options": {"temperature": 0.7, "num_predict": max_tokens},
        "stream": False,
    }

    try:
        print(f"🧠 Sending prompt to Ollama model='{model_name}' ...")
        resp = requests.post(url, json=payload, timeout=45)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, dict):
            for key in ("response", "text", "completion", "content", "output"):
                if key in data and isinstance(data[key], str):
                    return data[key].strip()
        return json.dumps(data)
    except Exception as e:
        print(f"⚠️ Ollama failed: {e}")
        return f"Error calling Ollama: {e}"


# === OPENROUTER FALLBACK (GLOBAL) ===
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
        print(f"🌐 Sending prompt to OpenRouter model='{OPENROUTER_MODEL}' ...")
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=120,
        )
        resp.raise_for_status()
        result = resp.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error calling OpenRouter: {e}"


# === HYBRID PARALLEL GENERATION ===
def generate_parallel(prompt: str, max_tokens: int = 512) -> str:
    """
    Run local (Ollama) and global (OpenRouter) generation in parallel.
    Returns whichever response arrives first.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(generate_with_ollama, prompt, max_tokens): "Ollama",
        }

        # Only add OpenRouter if key exists
        if OPENROUTER_KEY:
            futures[executor.submit(generate_with_openrouter, prompt, max_tokens)] = "OpenRouter"

        for future in concurrent.futures.as_completed(futures):
            model = futures[future]
            try:
                result = future.result(timeout=60)
                print(f"✅ {model} responded first.")
                return result
            except Exception as e:
                print(f"⚠️ {model} failed: {e}")
                continue

    return "❌ Both local and global models failed."


# === MAIN RAG PIPELINE ===
def answer_question(question: str, retriever_fn, k: int = 4) -> dict:
    """Main RAG function"""
    print(f"🔍 Retrieving top-{k} relevant chunks...")
    docs = retriever_fn(question, k=k)

    # ✅ Handle missing or empty context gracefully
    if not docs or len(docs) == 0:
        print("⚠️ No relevant context found.")
        return {
            "answer": (
                "I couldn’t find relevant information in your uploaded materials. "
                "Please upload a related PDF or ask a different question."
            ),
            "sources": [],
            "context": "",
        }

    context_text = _build_context_text(docs)
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=question)
    answer = generate_parallel(prompt)
    sources = [d.metadata for d in docs]
    print("✅ Answer generation complete.")
    print(answer)
    return {"answer": answer, "sources": sources, "context": context_text}
