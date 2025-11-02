# rag_core/vector_store.py
"""
Embedding + FAISS vector store manager using LangChain and HuggingFace embeddings.
We persist the FAISS index locally to a folder (faiss_index).
"""

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "faiss_index")  # ../faiss_index

def get_embeddings():
    # HuggingFaceEmbeddings wraps sentence-transformers model
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def build_faiss_from_chunks(chunks: list, persist: bool = True):
    """
    chunks: list of dicts {"page_content": str, "metadata": dict}
    Builds FAISS index and optionally persist.
    Returns the FAISS vectorstore object.
    """
    if not chunks:
        raise ValueError("No chunks provided to build the index.")

    embeddings = get_embeddings()
    docs = [Document(page_content=c["page_content"], metadata=c.get("metadata", {})) for c in chunks]
    faiss_store = FAISS.from_documents(docs, embeddings)

    if persist:
        # ensure directory exists
        os.makedirs(INDEX_DIR, exist_ok=True)
        faiss_store.save_local(INDEX_DIR)
    return faiss_store

def load_faiss_index():
    """Load persisted FAISS index. Returns None if not found."""
    from langchain_community.vectorstores import FAISS
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
    """Return top-k Document results for the query (if index exists)."""
    faiss_store = load_faiss_index()
    if faiss_store is None:
        return []
    return faiss_store.similarity_search(query, k=k)
