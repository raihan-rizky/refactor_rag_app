from abc import ABC, abstractmethod
from application import RAGResult
from typing import List

#'template' or abstract class for other classes
class EmbeddingModel(ABC):
    #function method as contract to enforce method implementation
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass
    #add status method with property decorator to increase readibility
    @property
    @abstractmethod
    def dimension(self) -> bool:
        pass

#Document store abstract class for memory and qdrant store class
class DocumentStore(ABC):
    @abstractmethod
    def add(self, text: str, embedding: List[float]) -> Document:
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], limit: int = 2) -> List[Document]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        pass

#Initiate RAG workflow abstract class for Lang Graph RAG
class RAGWorkFlow(ABC):
    @abstractmethod
    def invoke(self, question: str) -> RAGResult:
        pass

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        pass


