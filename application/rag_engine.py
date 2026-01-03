from domain import EmbeddingModel, RAGWorkFlow, DocumentStore, RAGResult, Document, StorageType
from typing import List

class RAGEngine:
    #Orchestrator for RAG Operations
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        document_store: DocumentStore,
        rag_workflow: RAGWorkFlow

    ):

        self._embedding_model = embedding_model
        self._document_store = document_store
        self._rag_workflow = rag_workflow

    def ask(self, question: str) -> RAGResult:
        return self._rag_workflow.invoke(question)

    def add_document(self, text: str) -> Document:

        embedding = self._embedding_model.embed(text)
        return self._document_store.add(embedding)
    
    @property
    def document_count(self) -> int:
        return self._document_store.count()

    @property
    def is_rag_engine_ready(self) -> bool:
        return self._rag_workflow.is_ready and self._document_store.is_ready

    @property
    def is_qdrant_ready(self) -> bool:
        if self._document_store.type == StorageType.QDRANT:
            return True
        else:
            return False