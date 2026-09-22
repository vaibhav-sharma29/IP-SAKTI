"""
Biopiracy Alerts — SQLite
"""

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_conn

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Biopiracy Alerts"])


class AlertResponse(BaseModel):
    id:               str
    patent_number:    str
    patent_title:     str
    applicant:        str
    filing_country:   str
    filing_date:      str
    tkdl_match:       str
    similarity_score: float
    status:           str
    action_deadline:  str
    source_url:       str
    is_read:          bool


DEMO_ALERTS = [
    {
        "id": "alert-001",
        "patent_number": "EP4123456A1",
        "patent_title": "Composition comprising Withania somnifera extract for cognitive enhancement",
        "applicant": "NovaBotanik GmbH, Germany",
        "filing_country": "European Patent Office (EPO)",
        "filing_date": "2024-03-15",
        "tkdl_match": "Charaka Samhita, Rasayana Adhyaya — Ashwagandha for medhya (cognitive) use. Documented circa 600 BCE.",
        "similarity_score": 0.91,
        "status": "open",
        "action_deadline": "2025-06-15",
        "source_url": "https://worldwide.espacenet.com/patent/search?q=EP4123456A1",
        "is_read": False
    },
    {
        "id": "alert-002",
        "patent_number": "US11234567B2",
        "patent_title": "Anti-inflammatory turmeric-black pepper synergistic formulation",
        "applicant": "HerbalPharm Inc., United States",
        "filing_country": "USPTO (United States)",
        "filing_date": "2024-01-22",
        "tkdl_match": "Sushruta Samhita — Haridra + Maricha for Shotha (inflammation). Documented circa 600 BCE.",
        "similarity_score": 0.87,
        "status": "open",
        "action_deadline": "2025-07-22",
        "source_url": "https://patents.google.com/patent/US11234567B2",
        "is_read": False
    },
    {
        "id": "alert-003",
        "patent_number": "WO2024198765A1",
        "patent_title": "Neem-based broad-spectrum antimicrobial composition",
        "applicant": "BioAgri Solutions Ltd., United Kingdom",
        "filing_country": "WIPO PCT Filing",
        "filing_date": "2024-06-10",
        "tkdl_match": "Ashtanga Hridayam — Nimba (Neem) as Krimighna (antimicrobial). Multiple classical refs pre-1000 CE.",
        "similarity_score": 0.94,
        "status": "open",
        "action_deadline": "2025-09-10",
        "source_url": "https://patentscope.wipo.int/search/en/WO2024198765",
        "is_read": False
    },
]


@router.get("/alerts", response_model=list[AlertResponse])
def list_alerts(status: str = "open"):
    conn = get_conn()
    cur = conn.cursor()
    if status == "all":
        cur.execute("SELECT * FROM biopiracy_alerts ORDER BY similarity_score DESC")
    else:
        cur.execute("SELECT * FROM biopiracy_alerts WHERE status=? ORDER BY similarity_score DESC", (status,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) | {"is_read": bool(r["is_read"])} for r in rows]


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM biopiracy_alerts WHERE id=?", (alert_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Alert not found")
    return dict(row) | {"is_read": bool(row["is_read"])}


@router.patch("/alerts/{alert_id}/read")
def mark_read(alert_id: str):
    conn = get_conn()
    conn.execute("UPDATE biopiracy_alerts SET is_read=1 WHERE id=?", (alert_id,))
    conn.commit()
    conn.close()
    return {"success": True}


@router.post("/alerts/seed")
def seed_demo_alerts():
    conn = get_conn()
    cur = conn.cursor()
    seeded = 0
    for a in DEMO_ALERTS:
        cur.execute("SELECT id FROM biopiracy_alerts WHERE id=?", (a["id"],))
        if not cur.fetchone():
            conn.execute(
                """INSERT INTO biopiracy_alerts
                   (id, patent_number, patent_title, applicant, filing_country,
                    filing_date, tkdl_match, similarity_score, status,
                    action_deadline, source_url, is_read, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (a["id"], a["patent_number"], a["patent_title"], a["applicant"],
                 a["filing_country"], a["filing_date"], a["tkdl_match"],
                 a["similarity_score"], a["status"], a["action_deadline"],
                 a["source_url"], int(a["is_read"]), datetime.utcnow().isoformat())
            )
            seeded += 1
    conn.commit()
    conn.close()
    return {"seeded": seeded, "message": f"{seeded} demo alerts added"}
