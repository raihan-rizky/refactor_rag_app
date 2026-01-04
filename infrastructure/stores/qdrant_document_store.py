from typing import List, Optional
from domain import DocumentStore, StorageType, Document
from infrastructure.embeddings import FakeEmbeddingService
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from application import QDRANT_COLLECTION_NAME, QDRANT_HOST, VECTOR_DIMENSION

class QdrantDocumentStore(DocumentStore):
    def __init__(
        self,
        host: str = QDRANT_HOST,
        collection_name: str = QDRANT_COLLECTION_NAME,
        vector_size: int = VECTOR_DIMENSION
    ):
        self._collection_name = collection_name
        self._vector_size = vector_size
        self._client: Optional[QdrantClient] = None
        self._doc_counter = 0
        self._initialize_client(host)
   
    #Connect to qdrant and preparing collection
    def _initialize_client(self, host: str) ->None:
        try:
            self._client = QdrantClient(host)
            self._client.recreate_collection(
                collection_name=self._collection_name,
                vectors_config=VectorParams(
                    size=self._vector_size,
                    distance=Distance.COSINE
                )
            )
        except Exception as e:
            print(f"[WARNING] Failed to initialize Qdrant: {e}")
            self._client = None
    #change text and vector to PointStruct format then save it to qdrant
    def add(self, text: str, embedding: List[float]) -> Document:
        if not self._client:
            raise RuntimeError("Qdrant client not initialized")
        doc_id = self._doc_counter
        self._doc_counter += 1
        self._client.upsert(
            collection_name=self._collection_name,
            points=[PointStruct(
                id=doc_id,
                vector=embedding,
                payload={"text": text}
            )]
        )

        doc = Document(id=doc_id, text=text)
        return doc
        
    #change user question into vector then do nearest neighbor in Qdrant and return Document as object
    def search(self, query_embedding: List[float], limit: int = 2) -> List[Document]:
        if not self._client:
            return []

        embedding = FakeEmbeddingService(query_embedding)
        hits = qdrant.search(collection_name=self._collection_name, query_vector=embedding, limit=limit)
        for hit in hits:
            doc = Document(id=hit.id, text=hit.payload["text"])
            results.append(doc)
        return results

    def count(self) -> int:
        return self._doc_counter
    
    #set store status avaiable
    @property
    def is_ready(self) -> bool:
        return self._client is not None

    #set StorageType to qdrant
    @property
    def type(self) -> StorageType:
        return StorageType.QDRANT
