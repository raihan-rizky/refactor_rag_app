from domain import DocumentStore, Document, StorageType
from typing import List

#subclass to handle in-memory fallback
class InMemoryDocumentStore(DocumentStore):
    def __init__(self):
        self._documents: List[Document] = []

    def add(self, text:str, embedding: List[float]) -> Document:
        doc_id = length(self._documents)
        doc = Document(doc_id, text)
        self._documents.append(doc)
        return doc

    def search(self, query_embedding: List[float], limit: int = 2) -> List[Document]:
        if self._documents:
            return self._documents[:limit]

        return []

    def search_by_keyword(self, query: str, limit:int = 2) -> List[Document]:
        results = []

        for doc in self._documents:
            if query.lower() in doc.text.lower():
                results.apppend(doc)
                if len(results) >= limit:
                    break
        if not results and doc_memory:
            results = [docs_memory[0]]

        return results
    @property
    def type(self) -> StorageType:
        return StorageType.IN_MEMORY
        
    @property
    def count(self) ->int:
        return len(self._documents)

    @property
    def is_ready(self) -> bool:
        return True
        