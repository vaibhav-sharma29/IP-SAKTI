"""
Chat History Service — MongoDB Atlas

Saves every conversation so:
1. Full audit trail (PS requirement)
2. Session restore possible
3. Analytics on most-asked questions
"""

import uuid
import logging
from datetime import datetime
from app.database import chat_sessions, chat_messages

logger = logging.getLogger(__name__)


async def get_or_create_session(
    session_id: str,
    language: str = "en",
    jurisdiction: str = "india"
) -> dict:
    """Get existing session or create new one in MongoDB"""
    col = chat_sessions()
    session = await col.find_one({"_id": session_id})

    if not session:
        session = {
            "_id":        session_id,
            "language":   language,
            "jurisdiction": jurisdiction,
            "created_at": datetime.utcnow().isoformat(),
        }
        await col.insert_one(session)
        logger.info(f"New session created: {session_id}")

    return session


async def save_message(
    session_id: str,
    role: str,
    content: str,
    sources: list = None,
    confidence: str = "medium",
    jurisdiction: str = "india"
) -> str:
    """Save one message to MongoDB. Returns message id."""
    msg_id = str(uuid.uuid4())
    col = chat_messages()

    await col.insert_one({
        "_id":          msg_id,
        "session_id":   session_id,
        "role":         role,           # "user" or "assistant"
        "content":      content,
        "sources":      sources or [],
        "confidence":   confidence,
        "jurisdiction": jurisdiction,
        "created_at":   datetime.utcnow().isoformat()
    })
    return msg_id


async def get_session_history(
    session_id: str,
    limit: int = 20
) -> list[dict]:
    """Get last N messages for a session — for chat restore"""
    col = chat_messages()
    cursor = col.find(
        {"session_id": session_id},
        {"_id": 0}
    ).sort("created_at", 1).limit(limit)

    messages = await cursor.to_list(length=limit)
    return messages
