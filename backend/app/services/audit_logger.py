"""
Audit Logger — DPDP Compliance (MongoDB)

Logs every API call — no raw query text stored (DPDP).
Query is SHA-256 hashed before storage.
"""

import time
import hashlib
import logging
from datetime import datetime
from app.database import audit_logs

logger = logging.getLogger(__name__)


async def log_request(
    endpoint: str,
    method: str,
    query: str = "",
    language: str = "en",
    jurisdiction: str = "india",
    confidence: str = "medium",
    latency_ms: float = 0.0,
    status_code: int = 200
) -> None:
    """Write audit log to MongoDB — never stores raw query text."""
    try:
        col = audit_logs()
        await col.insert_one({
            "endpoint":    endpoint,
            "method":      method,
            "jurisdiction": jurisdiction,
            "language":    language,
            "query_hash":  hashlib.sha256(query.encode()).hexdigest() if query else None,
            "confidence":  confidence,
            "latency_ms":  round(latency_ms, 2),
            "status_code": status_code,
            "timestamp":   datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.warning(f"Audit log failed (non-fatal): {e}")


class RequestTimer:
    """Measure API latency in milliseconds."""
    def __init__(self):
        self._start = time.perf_counter()

    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self._start) * 1000
