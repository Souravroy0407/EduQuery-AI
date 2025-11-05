# backend/rag_engine/rag_core/vector_store.py
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "faiss_index")

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def build_faiss_from_chunks(chunks: list, persist: bool = True):
    """
    Build or update FAISS index.
    If an index already exists, append new documents instead of replacing.
    """
    if not chunks:
        raise ValueError("No chunks provided to build the index.")

    embeddings = get_embeddings()
    docs = [Document(page_content=c["page_content"], metadata=c.get("metadata", {})) for c in chunks]

    os.makedirs(INDEX_DIR, exist_ok=True)
    index_exists = os.path.exists(os.path.join(INDEX_DIR, "index.faiss"))

    if index_exists:
        # ✅ Load existing index and append new docs
        print("📚 Existing FAISS index found. Appending new documents...")
        faiss_store = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
        faiss_store.add_documents(docs)
    else:
        # 🆕 Create a new one if it doesn’t exist
        print("🆕 Creating new FAISS index...")
        faiss_store = FAISS.from_documents(docs, embeddings)

    if persist:
        faiss_store.save_local(INDEX_DIR)
        print("✅ FAISS index saved/updated successfully at:", INDEX_DIR)

    return faiss_store

def load_faiss_index():
    embeddings = get_embeddings()
    print("🔍 Trying to load FAISS index from:", INDEX_DIR)

    if not os.path.isdir(INDEX_DIR):
        print("❌ FAISS folder missing:", INDEX_DIR)
        return None

    try:
        faiss_store = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
        print("✅ FAISS index loaded successfully.")
        return faiss_store
    except Exception as e:
        print("❌ Failed to load FAISS index:", e)
        return None

def query_faiss(query: str, k: int = 4):
    faiss_store = load_faiss_index()
    if faiss_store is None:
        return []
    return faiss_store.similarity_search(query, k=k)
