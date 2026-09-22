"""
SQLAlchemy Models — AWS PostgreSQL tables

Tables:
  chat_sessions   — every conversation stored (DPDP audit trail)
  chat_messages   — individual messages inside a session
  audit_logs      — every API call logged (PS requirement)
  biopiracy_alerts — flagged patent filings from WIPO monitor
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    String, Text, Boolean, DateTime, Float,
    ForeignKey, Integer, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


def new_uuid() -> str:
    return str(uuid.uuid4())


# ── Chat Sessions ─────────────────────────────────────────────
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id:         Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    language:   Mapped[str] = mapped_column(String(5),  default="en")
    jurisdiction: Mapped[str] = mapped_column(String(20), default="india")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan"
    )


# ── Chat Messages ─────────────────────────────────────────────
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id:           Mapped[str]   = mapped_column(String(36), primary_key=True, default=new_uuid)
    session_id:   Mapped[str]   = mapped_column(String(36), ForeignKey("chat_sessions.id"), nullable=False)
    role:         Mapped[str]   = mapped_column(String(20))    # "user" or "assistant"
    content:      Mapped[str]   = mapped_column(Text)
    sources:      Mapped[dict]  = mapped_column(JSON, default=list)   # list of {title, section, url}
    confidence:   Mapped[str]   = mapped_column(String(10), default="medium")
    jurisdiction: Mapped[str]   = mapped_column(String(20), default="india")
    created_at:   Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # relationship
    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")


# ── Audit Logs ────────────────────────────────────────────────
class AuditLog(Base):
    """
    DPDP (Digital Personal Data Protection) compliance.
    PS requirement: privacy + audit aligned to DPDP regime.
    Every API call logged — no PII stored, only metadata.
    """
    __tablename__ = "audit_logs"

    id:           Mapped[int]   = mapped_column(Integer, primary_key=True, autoincrement=True)
    endpoint:     Mapped[str]   = mapped_column(String(100))   # e.g. "/api/chat"
    method:       Mapped[str]   = mapped_column(String(10))    # GET / POST
    jurisdiction: Mapped[str]   = mapped_column(String(20), nullable=True)
    language:     Mapped[str]   = mapped_column(String(5),  nullable=True)
    query_hash:   Mapped[str]   = mapped_column(String(64), nullable=True)  # SHA256 of query — no raw text
    response_confidence: Mapped[str] = mapped_column(String(10), nullable=True)
    latency_ms:   Mapped[float] = mapped_column(Float, nullable=True)
    status_code:  Mapped[int]   = mapped_column(Integer, default=200)
    timestamp:    Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ── Biopiracy Alerts ──────────────────────────────────────────
class BiopiacyAlert(Base):
    """
    Stores flagged patent filings that may constitute biopiracy
    of Indian traditional knowledge.
    Populated by the biopiracy_monitor service (future cron job).
    """
    __tablename__ = "biopiracy_alerts"

    id:              Mapped[str]  = mapped_column(String(36), primary_key=True, default=new_uuid)
    patent_number:   Mapped[str]  = mapped_column(String(50))
    patent_title:    Mapped[str]  = mapped_column(Text)
    applicant:       Mapped[str]  = mapped_column(String(200), nullable=True)
    filing_country:  Mapped[str]  = mapped_column(String(100), nullable=True)
    filing_date:     Mapped[str]  = mapped_column(String(20),  nullable=True)
    tkdl_match:      Mapped[str]  = mapped_column(Text, nullable=True)   # Matching TKDL entry
    similarity_score: Mapped[float] = mapped_column(Float, default=0.0)  # 0-1
    status:          Mapped[str]  = mapped_column(String(20), default="open")  # open/resolved
    action_deadline: Mapped[str]  = mapped_column(String(20), nullable=True)   # Opposition window
    source_url:      Mapped[str]  = mapped_column(Text, nullable=True)
    created_at:      Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_read:         Mapped[bool] = mapped_column(Boolean, default=False)
