import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_db, close_db
from app.routes import chat, classify, health, alerts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Connecting to MongoDB Atlas...")
    await connect_db()
    logger.info("IP-SAKTI backend ready.")
    yield
    await close_db()
    logger.info("MongoDB connection closed.")


app = FastAPI(
    title="IP-SAKTI API",
    description="RAG-based AI assistant for Ayurveda IP & Regulatory Guidance | SIH 2026",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ip-sakti.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,   prefix="/api")
app.include_router(chat.router,     prefix="/api")
app.include_router(classify.router, prefix="/api")
app.include_router(alerts.router,   prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
