"""
Chat Route — POST /api/chat
GET  /api/chat/history/{session_id}

Complete flow:
1. Receive query from frontend
2. Translate if Hindi (Bhashini)
3. Save user message to PostgreSQL
4. Run RAG pipeline (LangChain + ChromaDB + Gemini)
5. Translate answer back if Hindi
6. Save AI answer to PostgreSQL
7. Write audit log (DPDP compliant — no raw PII)
8. Return structured response
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.rag_engine import get_rag_response
from app.services.translation import translate_to_english, translate_to_hindi
from app.services.chat_history import get_or_create_session, save_message, get_session_history
from app.services.audit_logger import log_request, RequestTimer

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Chat"])


# ── Request / Response models ────────────────────────────────

class ChatRequest(BaseModel):
    query:        str
    language:     str = "en"          # "en" or "hi"
    jurisdiction: str = "india"       # "india" | "international" | "both"
    session_id:   str = "default"

class Source(BaseModel):
    title:   str
    section: str = ""
    url:     str = ""

class ChatResponse(BaseModel):
    answer:       str
    sources:      list[Source]
    confidence:   str               # "high" | "medium" | "low"
    disclaimer:   str
    jurisdiction: str
    session_id:   str


# ── POST /api/chat ────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    timer = RequestTimer()
    status = 200

    try:
        # 1. Get or create session in DB
        await get_or_create_session(
            db,
            session_id=req.session_id,
            language=req.language,
            jurisdiction=req.jurisdiction
        )

        # 2. Translate query to English if Hindi
        english_query = req.query
        if req.language == "hi":
            english_query = await translate_to_english(req.query)

        # 3. Save user message to DB
        await save_message(
            db,
            session_id=req.session_id,
            role="user",
            content=req.query,       # store original language
            jurisdiction=req.jurisdiction
        )

        # 4. RAG pipeline
        result = await get_rag_response(
            query=english_query,
            jurisdiction=req.jurisdiction
        )

        # 5. Translate answer back if Hindi requested
        final_answer = result["answer"]
        if req.language == "hi":
            final_answer = await translate_to_hindi(result["answer"])

        # 6. Save AI answer to DB
        await save_message(
            db,
            session_id=req.session_id,
            role="assistant",
            content=final_answer,
            sources=result["sources"],
            confidence=result["confidence"],
            jurisdiction=req.jurisdiction
        )

        # 7. Audit log
        await log_request(
            db,
            endpoint="/api/chat",
            method="POST",
            query=req.query,
            language=req.language,
            jurisdiction=req.jurisdiction,
            confidence=result["confidence"],
            latency_ms=timer.elapsed_ms(),
            status_code=200
        )

        return ChatResponse(
            answer=final_answer,
            sources=[Source(**s) for s in result["sources"]],
            confidence=result["confidence"],
            disclaimer=(
                "⚠️ This is information only, not legal advice. "
                "Consult a qualified IP attorney for specific cases."
            ),
            jurisdiction=req.jurisdiction,
            session_id=req.session_id
        )

    except Exception as e:
        status = 500
        logger.error(f"Chat error: {e}")
        await log_request(
            db,
            endpoint="/api/chat",
            method="POST",
            query=req.query,
            language=req.language,
            jurisdiction=req.jurisdiction,
            latency_ms=timer.elapsed_ms(),
            status_code=500
        )
        raise HTTPException(status_code=500, detail="Internal server error. Please try again.")


# ── GET /api/chat/history/{session_id} ───────────────────────

@router.get("/chat/history/{session_id}")
async def get_history(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Returns previous messages for a session.
    Frontend uses this to restore chat on page reload.
    """
    history = await get_session_history(db, session_id)
    return {"session_id": session_id, "messages": history}
