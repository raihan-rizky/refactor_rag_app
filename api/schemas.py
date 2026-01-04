# Separated from routes for cleaner organization.

from pydantic import BaseModel
from typing import List


# Request Models

class QuestionRequest(BaseModel):
    question: str


class DocumentRequest(BaseModel):
    text: str



# Response Models

class QuestionResponse(BaseModel):
    question: str
    answer: str
    context_used: List[str]
    latency_sec: float


class DocumentResponse(BaseModel):
    id: int
    status: str


class StatusResponse(BaseModel):
    qdrant_ready: bool
    in_memory_docs_count: int
    graph_ready: bool