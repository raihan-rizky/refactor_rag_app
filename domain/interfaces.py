from abc import ABC, abstractmethod

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
    def add(self, text: str, embedding: List[float]) -> Document

