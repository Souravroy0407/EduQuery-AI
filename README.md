# 🧠 EduQuery AI  
### An AI-Powered Study Assistant using RAG (Retrieval-Augmented Generation)


---

## 📘 Overview

**EduQuery AI** is an AI-powered academic assistant that helps students interact intelligently with their study materials.  
It uses a **Retrieval-Augmented Generation (RAG)** pipeline to provide **context-based answers** directly from uploaded PDFs (notes, books, or research papers).

> Upload a PDF → Ask a question → Get an accurate, contextual AI-generated answer!

---

## 🧩 Features

- 📚 **Upload PDFs:** Upload one or multiple documents (notes or books).  
- 🧠 **RAG-based Retrieval:** Uses FAISS + HuggingFace embeddings for semantic document search.  
- ⚡ **Local & Cloud Models:** Works with **Ollama (Llama3 / Phi3)** locally, with **OpenRouter** as fallback.  
- 🧹 **Auto Cleanup:** Deletes processed PDFs after embedding creation to save disk space.  
- 💬 **Smart Fallback:** Returns professional messages when context isn’t found.  
- 🖥️ **Frontend Integration:** Built for React frontend + Django backend.

---

## ⚙️ Architecture

            ┌──────────────────────┐
            │   React Frontend     │
            └─────────┬────────────┘
                      │  (API Calls)
            ┌─────────▼────────────┐
            │   Django Backend     │
            │  (rag_engine app)    │
            └─────────┬────────────┘
                      │
    ┌─────────────────┼──────────────────┐
    │                 │                  │
┌───────▼───────┐ ┌───────▼────────┐ ┌───────▼──────────────┐
│ PDF Loader │ │ Vector Store │ │ QA Engine (LLM) │
│ (PyMuPDF) │ │ (FAISS Index) │ │ (Ollama/OpenRouter) │
└────────────────┘ └────────────────┘ └──────────────────────┘


---

## 🧠 Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend Framework** | Django REST Framework |
| **Frontend** | React.js |
| **Embeddings** | HuggingFace SentenceTransformer |
| **Vector Database** | FAISS |
| **Local LLM** | Ollama (Llama3 / Phi3) |
| **Cloud LLM (Fallback)** | OpenRouter (DeepSeek) |
| **PDF Parsing** | PyMuPDF (fitz) |
| **RAG Framework** | LangChain |

---

## 🧾 Project Structure

EduQueryAI/
│
├── backend/
│ ├── rag_engine/
│ │ ├── views.py
│ │ ├── urls.py
│ │ ├── rag_core/
│ │ │ ├── pdf_loader.py
│ │ │ ├── vector_store.py
│ │ │ ├── qa_engine.py
│ │ └── uploaded_pdfs/
│ │
│ └── manage.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── api.js
│   └── package.json
│
└── README.md

🧪 Example Response

Question:

What is photosynthesis?

Answer:

Photosynthesis is the process by which green plants convert sunlight, water, and carbon dioxide into glucose and oxygen. It occurs mainly in the chloroplasts of plant cells (from your uploaded document). 🌱