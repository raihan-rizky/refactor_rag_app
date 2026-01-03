from domain import EmbeddingModel
from application VECTOR_DIMENSION
from typing import List
import random

#fake embedding service using EmbeddingModel abstract class
class FakeEmbeddingService(EmbeddingModel):
    VECTOR_DIMENSION = VECTOR_DIMENSION
    def __init__(self, 
        seed_modulo: int = 10000) -> None:
        self._seed_modulo = seed_modulo
    def embed(self, text: str) -> List[float]:
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(128)]
    @property
    def dimension(self) -> int:
        return self.VECTOR_DIMENSION

