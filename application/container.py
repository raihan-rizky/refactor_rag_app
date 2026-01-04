"""
-Dependency Injection Container
-Central hub for creating components and wiring them up.
"""
from typing import Optional
from domain import DocumentStore, EmbeddingModel, RAGWorkFlow
from .config import QDRANT_HOST, QDRANT_COLLECTION_NAME, VECTOR_DIMENSION

#create an embbeder instance
def create_embedder() -> "Embedder":
    from infrastructure.embeddings import FakeEmbeddingService

    return FakeEmbeddingService()
 
# try to connect qdrant first, if it fail then fallback to in-memory
def create_document_store(vector_size: Optional[int]) ->"DocumentStore":
    from infrastructure.stores import InMemoryDocumentStore, QdrantDocumentStore

    size = vector_size or VECTOR_DIMENSION

    try:
        store = QdrantDocumentStore(
            host= QDRANT_HOST,
            collection_name = QDRANT_COLLECTION_NAME,
            vector_size = size

        )

        if store.is_ready:
            print("Connected to Qdrant")
            return store
    except Exception as e:
        print(f"⚠️  Qdrant not available. Falling back to in-memory list: {e}")
    print("Using in memory document store")
    return InMemoryDocumentStore()

#build default workflow with LangGraphRAG
def create_workflow(
    embedder: "EmbeddingModel",
    document_store: "DocumentStore"
) -> "RAGWorkFlow":

    from infrastructure.workflow import LangGraphRAG

    return LangGraphRAG(
        embedding_model=embedder,
        document_store=document_store
    )


#create RAG Engine instance with complete dependency
def create_rag_engine(
    embedder: Optional["EmbeddingModel"] = None,
    document_store: Optional["DocumentStore"] = None,
    workflow: Optional["RAGWorkFlow"] = None
):
    from application import RAGEngine

    embedder = embedder or create_embedder()
    document_store = document_store or create_document_store()
    workflow = workflow or create_workflow(embedder, document_store)

    return RAGEngine(
        embedder,
        document_store,
        workflow
    )

