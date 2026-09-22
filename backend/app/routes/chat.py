"""
Chat Route — POST /api/chat
GET  /api/chat/history/{session_id}
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag_engine import get_rag_response
from app.services.translation import translate_to_english, translate_to_hindi
from app.services.chat_history import get_or_create_session, save_message, get_session_history
from app.services.audit_logger import log_request, RequestTimer

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Chat"])


# ── Models ───────────────────────────────────────────────────

class ChatRequest(BaseModel):
    query:        str
    language:     str = "en"
    jurisdiction: str = "india"
    session_id:   str = "default"

class Source(BaseModel):
    title:   str
    section: str = ""
    url:     str = ""

class ChatResponse(BaseModel):
    answer:       str
    sources:      list[Source]
    confidence:   str
    disclaimer:   str
    jurisdiction: str
    session_id:   str


# ── POST /api/chat ────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    timer = RequestTimer()
    try:
        # 1. Get/create session
        await get_or_create_session(
            req.session_id, req.language, req.jurisdiction
        )

        # 2. Translate if Hindi
        english_query = req.query
        if req.language == "hi":
            english_query = await translate_to_english(req.query)

        # 3. Save user message
        await save_message(
            session_id=req.session_id,
            role="user",
            content=req.query,
            jurisdiction=req.jurisdiction
        )

        # 4. RAG pipeline
        result = await get_rag_response(
            query=english_query,
            jurisdiction=req.jurisdiction
        )

        # 5. Translate answer back if Hindi
        final_answer = result["answer"]
        if req.language == "hi":
            final_answer = await translate_to_hindi(result["answer"])

        # 6. Save AI answer
        await save_message(
            session_id=req.session_id,
            role="assistant",
            content=final_answer,
            sources=result["sources"],
            confidence=result["confidence"],
            jurisdiction=req.jurisdiction
        )

        # 7. Audit log
        await log_request(
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
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /api/chat/history/{session_id} ───────────────────────

@router.get("/chat/history/{session_id}")
async def get_history(session_id: str):
    history = await get_session_history(session_id)
    return {"session_id": session_id, "messages": history}
