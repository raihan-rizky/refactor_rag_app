from fastapi import FastAPI

from api import router

#Application factory that creates and configures the FastAPI app.
def create_app() -> FastAPI:
    app = FastAPI(
        title="Learning RAG Demo",
        description="A refactored RAG service with clean architecture",
        version="3.0.0"
    )
    
    # Include API routes
    app.include_router(router)
    
    return app


# Create the app instance for uvicorn
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)