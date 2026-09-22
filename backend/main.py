import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import chat, classify, health, alerts, abs_checker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing SQLite database...")
    init_db()
    logger.info("Pre-loading embedding model...")
    # Load embedding model at startup so first request is fast
    import asyncio
    loop = asyncio.get_event_loop()
    from app.services.rag_engine import _get_embeddings, _get_india_vectorstore, _get_international_vectorstore
    await loop.run_in_executor(None, _get_india_vectorstore)
    await loop.run_in_executor(None, _get_international_vectorstore)
    logger.info("IP-SAKTI backend ready — all models loaded.")
    yield
    logger.info("IP-SAKTI backend shutting down.")


app = FastAPI(
    title="IP-SAKTI API",
    description="RAG-based AI assistant for Ayurveda IP | SIH 2026",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,       prefix="/api")
app.include_router(chat.router,         prefix="/api")
app.include_router(classify.router,     prefix="/api")
app.include_router(alerts.router,       prefix="/api")
app.include_router(abs_checker.router,  prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
