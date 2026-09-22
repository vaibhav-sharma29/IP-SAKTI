"""
Chat History Service — SQLite
"""

import json
import uuid
from datetime import datetime
from app.database import get_conn


def get_or_create_session(
    session_id: str,
    language: str = "en",
    jurisdiction: str = "india"
) -> dict:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM chat_sessions WHERE id = ?", (session_id,))
    session = cur.fetchone()

    if not session:
        now = datetime.utcnow().isoformat()
        cur.execute(
            "INSERT INTO chat_sessions (id, language, jurisdiction, created_at) VALUES (?,?,?,?)",
            (session_id, language, jurisdiction, now)
        )
        conn.commit()

    conn.close()
    return {"id": session_id, "language": language, "jurisdiction": jurisdiction}


def save_message(
    session_id: str,
    role: str,
    content: str,
    sources: list = None,
    confidence: str = "medium",
    jurisdiction: str = "india"
) -> str:
    msg_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    conn = get_conn()
    conn.execute(
        """INSERT INTO chat_messages
           (id, session_id, role, content, sources, confidence, jurisdiction, created_at)
           VALUES (?,?,?,?,?,?,?,?)""",
        (msg_id, session_id, role, content,
         json.dumps(sources or []), confidence, jurisdiction, now)
    )
    conn.commit()
    conn.close()
    return msg_id


def get_session_history(session_id: str, limit: int = 20) -> list[dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """SELECT role, content, sources, confidence, created_at
           FROM chat_messages WHERE session_id = ?
           ORDER BY created_at ASC LIMIT ?""",
        (session_id, limit)
    )
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "role":       row["role"],
            "content":    row["content"],
            "sources":    json.loads(row["sources"] or "[]"),
            "confidence": row["confidence"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]
