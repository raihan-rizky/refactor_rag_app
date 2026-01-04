import time
from fastapi import APIRouter, HTTPException, Depends
from .schemas import (
    QuestionRequest, QuestionResponse,
    DocumentRequest, DocumentResponse,
    StatusResponse

)
from application import RAGEngine
from .deps import get_rag_engine
# --API Routes--

router = APIRouter()


@router.post("/ask", response_model=QuestionResponse)
def ask_question(
    req: QuestionRequest,
    engine: RAGEngine = Depends(get_rag_engine)

) -> QuestionResponse:

    start = time.time()
    try:
        result = engine.ask(req.question)
        return QuestionResponse(
            question=req.question,
            answer=result.answer,
            context_used=[doc.text for doc in result.context],
            latency_sec=round(time.time() - start, 3)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add", response_model=DocumentResponse)
def add_document(
    req: DocumentRequest,
    engine: RAGEngine = Depends(get_rag_engine)
) -> DocumentResponse:
    
    try:
        result = engine.add_document(req.text)
        return DocumentResponse(
            id=result.id,
            status="added"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/status", response_model=StatusResponse)
def status(
    engine: RAGEngine = Depends(get_rag_engine)
) -> StatusResponse:
    return StatusResponse(
        document_count= engine.document_count,
        engine_ready = engine.is_ready,
        qdrant_ready = engine.is_qdrant_ready
        
    )