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
    document_count: int
    engine_ready: bool
    qdrant_ready: bool