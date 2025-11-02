# rag_engine/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import json

from .rag_core.pdf_loader import extract_text_from_pdf, chunk_text
from .rag_core.vector_store import build_faiss_from_chunks, load_faiss_index, query_faiss
from .rag_core.qa_engine import answer_question

# folder to save uploaded PDFs temporarily
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploaded_pdfs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@csrf_exempt
def upload_pdf(request):
    """
    POST endpoint to upload a PDF file.
    - saves file
    - extracts text
    - chunks and builds/updates FAISS index (overwrites existing)
    """
    if request.method != "POST":
        return JsonResponse({"error": "Use POST to upload a PDF."}, status=405)

    file = request.FILES.get("file")
    if not file:
        return JsonResponse({"error": "No file in request under key 'file'."}, status=400)

    # save file
    file_name = default_storage.save(os.path.join("rag_engine", "uploaded_pdfs", file.name), ContentFile(file.read()))
    file_path = os.path.join(settings.BASE_DIR, file_name) if hasattr(settings, "BASE_DIR") else os.path.abspath(file_name)

    # extract text
    try:
        text = extract_text_from_pdf(file_path)
        chunks = chunk_text(text)
        # attach source metadata
        for i, c in enumerate(chunks):
            c["metadata"]["source"] = file.name
        # build FAISS index (overwrite)
        build_faiss_from_chunks(chunks, persist=True)
        return JsonResponse({"status": "ok", "message": "PDF processed and vector store built", "file": file.name})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def query_knowledge(request):
    """
    POST endpoint: {"question": "..."}
    Returns: {"answer": "...", "sources": [...], "context": "..."}
    """
    if request.method != "POST":
        return JsonResponse({"error": "Use POST with JSON {\"question\": \"...\"}"}, status=405)

    try:
        body = json.loads(request.body)
        question = body.get("question", "").strip()
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not question:
        return JsonResponse({"error": "Missing 'question' in request JSON."}, status=400)

    # Check FAISS exists
    faiss = load_faiss_index()
    if faiss is None:
        return JsonResponse({"error": "No index found. Upload PDFs first."}, status=400)

    try:
        result = answer_question(question, retriever_fn=query_faiss, k=4)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
