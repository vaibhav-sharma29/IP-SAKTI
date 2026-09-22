"""
Database — SQLite (zero setup, works everywhere)

For hackathon: SQLite is perfect.
- No cloud account needed
- No configuration needed
- Works locally AND on Render/Railway deployment
- File: backend/ipsakti.db (auto-created)
"""

import sqlite3
import os
import json
import uuid
import hashlib
from datetime import datetime

DB_PATH = os.environ.get("DB_PATH", "./ipsakti.db")


def get_conn():
    """Get SQLite connection — creates DB file if not exists"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # dict-like rows
    conn.execute("PRAGMA journal_mode=WAL")  # better concurrency
    return conn


def init_db():
    """Create all tables — called once on startup"""
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id           TEXT PRIMARY KEY,
            language     TEXT DEFAULT 'en',
            jurisdiction TEXT DEFAULT 'india',
            created_at   TEXT
        );

        CREATE TABLE IF NOT EXISTS chat_messages (
            id           TEXT PRIMARY KEY,
            session_id   TEXT,
            role         TEXT,
            content      TEXT,
            sources      TEXT,
            confidence   TEXT DEFAULT 'medium',
            jurisdiction TEXT DEFAULT 'india',
            created_at   TEXT
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint     TEXT,
            method       TEXT,
            jurisdiction TEXT,
            language     TEXT,
            query_hash   TEXT,
            confidence   TEXT,
            latency_ms   REAL,
            status_code  INTEGER,
            timestamp    TEXT
        );

        CREATE TABLE IF NOT EXISTS biopiracy_alerts (
            id               TEXT PRIMARY KEY,
            patent_number    TEXT,
            patent_title     TEXT,
            applicant        TEXT,
            filing_country   TEXT,
            filing_date      TEXT,
            tkdl_match       TEXT,
            similarity_score REAL,
            status           TEXT DEFAULT 'open',
            action_deadline  TEXT,
            source_url       TEXT,
            is_read          INTEGER DEFAULT 0,
            created_at       TEXT
        );
    """)

    conn.commit()
    conn.close()
    print(f"SQLite DB ready: {DB_PATH}")
