from domain import DocumentStore, Document, StorageType
from typing import List, Optional

#subclass to handle in-memory fallback
class InMemoryDocumentStore(DocumentStore):
    def __init__(self):
        self._documents: List[Document] = []

    def add(self, text:str, embedding: List[float]) -> Document:
        doc_id = len(self._documents)
        doc = Document(doc_id, text)
        self._documents.append(doc)
        return doc

    def search(self, query_embedding: List[float], limit: int = 2, query_text: Optional[str] = None) -> List[Document]:
        results = []
        if query_text and self._documents:
            for doc in self._documents:
                if query_text.lower() in doc.text.lower():
                    results.append(doc)
                    if len(results) >= limit:
                        break
        if not results and self._documents:
            results = [self._documents[0]]
        return results

    def search_by_keyword(self, query: str, limit:int = 2) -> List[Document]:
        results = []

        for doc in self._documents:
            if query.lower() in doc.text.lower():
                results.append(doc)
                if len(results) >= limit:
                    break

        return results
    @property
    def type(self) -> StorageType:
        return StorageType.IN_MEMORY
        
    def count(self) ->int:
        return len(self._documents)

    @property
    def is_ready(self) -> bool:
        return True
        