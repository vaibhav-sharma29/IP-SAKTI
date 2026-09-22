"""
Audit Logger — DPDP Compliance Service

PS requirement:
  "privacy, audit and security aligned to the
   Digital Personal Data Protection regime"

What we log:
  - Which endpoint was called
  - Language + jurisdiction (no PII)
  - SHA-256 hash of query (not raw text — DPDP)
  - Response confidence + latency
  - HTTP status code

What we NEVER log:
  - Raw query text
  - User IP address
  - Any personally identifiable information
"""

import time
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import AuditLog
from app.services.rag_engine import hash_query

logger = logging.getLogger(__name__)


async def log_request(
    db: AsyncSession,
    endpoint: str,
    method: str,
    query: str = "",
    language: str = "en",
    jurisdiction: str = "india",
    confidence: str = "medium",
    latency_ms: float = 0.0,
    status_code: int = 200
) -> None:
    """
    Write one audit log entry.
    Raw query is hashed — never stored as plaintext (DPDP).
    Fire-and-forget — errors here should NOT crash the main request.
    """
    try:
        entry = AuditLog(
            endpoint=endpoint,
            method=method,
            jurisdiction=jurisdiction,
            language=language,
            query_hash=hash_query(query) if query else None,
            response_confidence=confidence,
            latency_ms=round(latency_ms, 2),
            status_code=status_code
        )
        db.add(entry)
        await db.flush()
    except Exception as e:
        # Never crash the main request because of audit failure
        logger.warning(f"Audit log write failed (non-fatal): {e}")


class RequestTimer:
    """
    Simple context manager to measure API latency.

    Usage:
        timer = RequestTimer()
        # ... do work ...
        latency = timer.elapsed_ms()
    """
    def __init__(self):
        self._start = time.perf_counter()

    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self._start) * 1000
