from fastapi import FastAPI

from app.api import chat_router
from app.core.settings import settings
from app.utils import lifespan


app = FastAPI(
    title="Chat API - Strands + Ollama",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(chat_router)


@app.get("/health", tags=["infra"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
