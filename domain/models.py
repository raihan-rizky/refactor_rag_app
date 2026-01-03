from dataclasses import dataclass
from typing import List

#dataclass to reduce boilerplate and increase readability
@dataclass
class Document:
    id: int
    text: str
@dataclass
class RAGResult:
    question: str
    answer: str
    context: List[str]