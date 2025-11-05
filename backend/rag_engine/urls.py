# rag_engine/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('query/', views.query_knowledge, name='query_knowledge'),
]
