"""
Chat History Service — AWS PostgreSQL

Saves every conversation to DB so:
1. User can continue previous sessions (future feature)
2. Full audit trail exists (PS requirement)
3. Analytics possible — most asked questions, etc.
"""

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models import ChatSession, ChatMessage

logger = logging.getLogger(__name__)


async def get_or_create_session(
    db: AsyncSession,
    session_id: str,
    language: str = "en",
    jurisdiction: str = "india"
) -> ChatSession:
    """
    Get existing session or create new one.
    Called at start of every /api/chat request.
    """
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        session = ChatSession(
            id=session_id,
            language=language,
            jurisdiction=jurisdiction
        )
        db.add(session)
        await db.flush()   # get DB id without full commit
        logger.info(f"New chat session created: {session_id}")

    return session


async def save_message(
    db: AsyncSession,
    session_id: str,
    role: str,
    content: str,
    sources: list = None,
    confidence: str = "medium",
    jurisdiction: str = "india"
) -> ChatMessage:
    """
    Save one message (user or assistant) to DB.
    Called twice per /api/chat — once for user query, once for AI answer.
    """
    msg = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        sources=sources or [],
        confidence=confidence,
        jurisdiction=jurisdiction
    )
    db.add(msg)
    await db.flush()
    return msg


async def get_session_history(
    db: AsyncSession,
    session_id: str,
    limit: int = 20
) -> list[dict]:
    """
    Retrieve last N messages for a session.
    Used by frontend to restore chat on page reload (future).

    Returns list of { role, content, sources, confidence, created_at }
    """
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
        .limit(limit)
    )
    messages = result.scalars().all()

    return [
        {
            "role":       msg.role,
            "content":    msg.content,
            "sources":    msg.sources,
            "confidence": msg.confidence,
            "created_at": msg.created_at.isoformat()
        }
        for msg in messages
    ]
