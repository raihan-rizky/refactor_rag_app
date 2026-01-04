from functools import lru_cache
from domain import EmbeddingModel, DocumentStore, RAGWorkFlow
from application.rag_engine import RAGEngine
from application import create_embedder, create_document_store, create_rag_engine, create_workflow

#cache to avoid reload and reconnect every single time
@lru_cache()
def get_embedder() -> EmbeddingModel:
    return create_embedder()


@lru_cache()
def get_document_store() -> DocumentStore:
    embedder = get_embedder()
    return create_document_store(embedder.dimension)

@lru_cache()
def get_worfkflow() -> RAGWorkFlow:
    return create_worfkflow(
        embedder=get_embedder(),
        document_store=get_document_store()
    )

@lru_cache()
def get_rag_engine() -> RAGEngine:
    embedder = get_embedder()
    document_store = get_document_store()

    return create_rag_engine(
        embedder=embedder,
        document_store=document_store,
        workflow = create_workflow(embedder, document_store)
    )
