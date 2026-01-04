## Refactored RAG App

Refactored version of the simple RAG following clean architecture principles.

See [notes.md](./notes.md) for main design decisions, trade-offs, and how this version improves maintainability.

## Project Structure

```
├── api/ # HTTP routes & schemas
├── application/ # Business logic (RAGEngine)
├── domain/ # Abstract interfaces
├── infrastructure/# Concrete implementations
└── main.py # Entry point
```

## Requirements

- Python 3.10+
- FastAPI
- LangGraph
- Qdrant (optional, falls back to in-memory)

## How to Run

```bash
uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description  |
| ------ | -------- | ------------ |
| POST   | /add     | Add document |
| POST   | /ask     | Ask question |
| GET    | /status  | Check status |
