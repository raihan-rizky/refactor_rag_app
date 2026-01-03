"""
-Dependency Injection Container
-Central hub for creating components and wiring them up.
"""
from typing import Optional
from domain import DocumentStore, EmbeddingModel, RAGWorkFlow
from .config import QDRANT_HOST, COLLECTION_NAME, VECTOR_DIMENSION

def create_rag_engine(
    embedder: Optional["EmbeddingService"] = None,
    document_store: Optional["DocumentStore"] = None,
    workflow: Optional["RAGWorkFlow"] = None
):
    from application import RAGEngine

    return RAGEngine(
        embedder,
        document_store,
        workflow
    )