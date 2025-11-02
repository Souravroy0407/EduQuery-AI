# rag_core/pdf_loader.py
"""
PDF loader: extract text from PDFs using PyMuPDF (fitz)
and produce a list of document chunks (simple chunking).
"""

import fitz  # PyMuPDF
import math
import re

def extract_text_from_pdf(path: str) -> str:
    """Extract all text from a PDF file path."""
    doc = fitz.open(path)
    pages = []
    for page in doc:
        text = page.get_text("text")
        pages.append(text)
    doc.close()
    return "\n".join(pages)

def clean_text(text: str) -> str:
    """Basic cleanup (strip repeated whitespace)."""
    # remove strange control characters
    text = re.sub(r"\s+", " ", text).strip()
    return text

def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 200):
    """
    Simple sliding-window chunking.
    chunk_size = ~approx number of tokens/characters (we use characters here for simplicity).
    Returns list of dicts: {"page_content": ..., "metadata": {...}}
    """
    text = clean_text(text)
    n = len(text)
    if n == 0:
        return []

    chunks = []
    start = 0
    chunk_id = 0
    while start < n:
        end = start + chunk_size
        chunk = text[start:end]
        metadata = {"chunk_id": chunk_id}
        chunks.append({"page_content": chunk, "metadata": metadata})
        chunk_id += 1
        # advance with overlap
        start = end - chunk_overlap if (end - chunk_overlap) > start else end

    return chunks
