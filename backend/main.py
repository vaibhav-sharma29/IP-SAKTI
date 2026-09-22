"""
IP-SAKTI Backend — FastAPI Application Entry Point

Startup sequence:
1. Connect to AWS PostgreSQL (RDS)
2. Create tables if they don't exist
3. Register all routes
4. Start server
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import chat, classify, health, alerts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


# ── Lifespan — runs on startup and shutdown ──────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    logger.info("IP-SAKTI backend starting...")
    logger.info("Connecting to PostgreSQL (AWS RDS)...")
    await init_db()
    logger.info("Database tables ready.")
    logger.info("IP-SAKTI backend ready.")
    yield
    # SHUTDOWN
    logger.info("IP-SAKTI backend shutting down.")


# ── FastAPI app ───────────────────────────────────────────────
app = FastAPI(
    title="IP-SAKTI API",
    description=(
        "RAG-based AI assistant for Ayurveda IP & Regulatory Guidance. "
        "SIH 2026 | Ministry of Ayush | PS ID: SIH26045"
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",       # Swagger UI at /docs
    redoc_url="/redoc"      # ReDoc at /redoc
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",         # Local dev
        "https://ip-sakti.vercel.app",   # Production frontend (update when deployed)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────
app.include_router(health.router,   prefix="/api")
app.include_router(chat.router,     prefix="/api")
app.include_router(classify.router, prefix="/api")
app.include_router(alerts.router,   prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
