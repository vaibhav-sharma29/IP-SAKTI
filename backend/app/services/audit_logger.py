"""
Audit Logger — SQLite (DPDP compliant)
"""

import time
import hashlib
from datetime import datetime
from app.database import get_conn


def log_request(
    endpoint: str,
    method: str,
    query: str = "",
    language: str = "en",
    jurisdiction: str = "india",
    confidence: str = "medium",
    latency_ms: float = 0.0,
    status_code: int = 200
) -> None:
    try:
        conn = get_conn()
        conn.execute(
            """INSERT INTO audit_logs
               (endpoint, method, jurisdiction, language,
                query_hash, confidence, latency_ms, status_code, timestamp)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                endpoint, method, jurisdiction, language,
                hashlib.sha256(query.encode()).hexdigest() if query else None,
                confidence, round(latency_ms, 2), status_code,
                datetime.utcnow().isoformat()
            )
        )
        conn.commit()
        conn.close()
    except Exception as e:
        pass   # Never crash main request for audit failure


class RequestTimer:
    def __init__(self):
        import time
        self._start = time.perf_counter()

    def elapsed_ms(self) -> float:
        import time
        return (time.perf_counter() - self._start) * 1000
