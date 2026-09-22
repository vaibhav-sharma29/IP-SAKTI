"""
Biopiracy Alerts Route

GET  /api/alerts          — list all open alerts
GET  /api/alerts/{id}     — single alert detail
POST /api/alerts/seed     — seed demo alerts (hackathon demo use)
PATCH /api/alerts/{id}/read — mark alert as read

What is biopiracy?
  When a foreign entity patents India's traditional knowledge
  (Neem, Turmeric, Basmati cases are real historical examples).
  IP-SAKTI monitors WIPO patent filings and flags suspicious ones.

For hackathon: We seed realistic demo data.
In production: A cron job would scrape WIPO + Google Patents daily.
"""

import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.database import get_db
from app.models import BiopiacyAlert

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Biopiracy Alerts"])


# ── Response model ────────────────────────────────────────────

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
    created_at:       str

    class Config:
        from_attributes = True


# ── Demo seed data — realistic hackathon examples ─────────────

DEMO_ALERTS = [
    {
        "id": "alert-001",
        "patent_number": "EP4123456A1",
        "patent_title": "Composition comprising Withania somnifera extract for cognitive enhancement",
        "applicant": "NovaBotanik GmbH, Germany",
        "filing_country": "European Patent Office (EPO)",
        "filing_date": "2024-03-15",
        "tkdl_match": "Charaka Samhita, Rasayana Adhyaya — Ashwagandha (Withania somnifera) for medhya (cognitive) use. Documented circa 600 BCE.",
        "similarity_score": 0.91,
        "status": "open",
        "action_deadline": "2025-01-15",
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
        "tkdl_match": "Sushruta Samhita, Chikitsa Sthana — Haridra (Turmeric) + Maricha (Black Pepper) combination for Shotha (inflammation). Documented circa 600 BCE.",
        "similarity_score": 0.87,
        "status": "open",
        "action_deadline": "2025-03-22",
        "source_url": "https://patents.google.com/patent/US11234567B2",
        "is_read": False
    },
    {
        "id": "alert-003",
        "patent_number": "WO2024198765A1",
        "patent_title": "Neem-based broad-spectrum antimicrobial composition and method of preparation",
        "applicant": "BioAgri Solutions Ltd., United Kingdom",
        "filing_country": "WIPO PCT Filing",
        "filing_date": "2024-06-10",
        "tkdl_match": "Ashtanga Hridayam, Uttara Sthana — Nimba (Neem / Azadirachta indica) as Krimighna (antimicrobial). Multiple classical references pre-1000 CE.",
        "similarity_score": 0.94,
        "status": "open",
        "action_deadline": "2025-06-10",
        "source_url": "https://patentscope.wipo.int/search/en/WO2024198765",
        "is_read": False
    },
    {
        "id": "alert-004",
        "patent_number": "EP3987654B1",
        "patent_title": "Bacopa monnieri standardized extract for memory and learning improvement",
        "applicant": "CogniBotanica SA, France",
        "filing_country": "European Patent Office (EPO)",
        "filing_date": "2023-11-05",
        "tkdl_match": "Charaka Samhita, Kalpasthana — Brahmi (Bacopa monnieri) as Medhya Rasayana for Smritiprada (memory enhancement).",
        "similarity_score": 0.89,
        "status": "resolved",
        "action_deadline": "2024-11-05",
        "source_url": "https://worldwide.espacenet.com/patent/search?q=EP3987654B1",
        "is_read": True
    },
]


# ── GET /api/alerts ───────────────────────────────────────────

@router.get("/alerts", response_model=list[AlertResponse])
async def list_alerts(
    status: str = "open",
    db: AsyncSession = Depends(get_db)
):
    """
    List biopiracy alerts filtered by status.
    Query param: ?status=open (default) | resolved | all

    Frontend shows these as warning cards with:
    - Patent title + applicant
    - TKDL match highlighted
    - Similarity score as progress bar
    - Action deadline countdown
    - Opposition guide link
    """
    query = select(BiopiacyAlert)
    if status != "all":
        query = query.where(BiopiacyAlert.status == status)
    query = query.order_by(BiopiacyAlert.similarity_score.desc())

    result = await db.execute(query)
    alerts = result.scalars().all()

    return [
        AlertResponse(
            id=a.id,
            patent_number=a.patent_number,
            patent_title=a.patent_title,
            applicant=a.applicant or "",
            filing_country=a.filing_country or "",
            filing_date=a.filing_date or "",
            tkdl_match=a.tkdl_match or "",
            similarity_score=a.similarity_score,
            status=a.status,
            action_deadline=a.action_deadline or "",
            source_url=a.source_url or "",
            is_read=a.is_read,
            created_at=a.created_at.isoformat()
        )
        for a in alerts
    ]


# ── GET /api/alerts/{id} ──────────────────────────────────────

@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Single alert detail — frontend opens on card click"""
    result = await db.execute(
        select(BiopiacyAlert).where(BiopiacyAlert.id == alert_id)
    )
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    return AlertResponse(
        id=alert.id,
        patent_number=alert.patent_number,
        patent_title=alert.patent_title,
        applicant=alert.applicant or "",
        filing_country=alert.filing_country or "",
        filing_date=alert.filing_date or "",
        tkdl_match=alert.tkdl_match or "",
        similarity_score=alert.similarity_score,
        status=alert.status,
        action_deadline=alert.action_deadline or "",
        source_url=alert.source_url or "",
        is_read=alert.is_read,
        created_at=alert.created_at.isoformat()
    )


# ── PATCH /api/alerts/{id}/read ───────────────────────────────

@router.patch("/alerts/{alert_id}/read")
async def mark_read(
    alert_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Mark alert as read — frontend calls on card open"""
    await db.execute(
        update(BiopiacyAlert)
        .where(BiopiacyAlert.id == alert_id)
        .values(is_read=True)
    )
    return {"success": True}


# ── POST /api/alerts/seed ─────────────────────────────────────

@router.post("/alerts/seed")
async def seed_demo_alerts(db: AsyncSession = Depends(get_db)):
    """
    Seeds realistic demo biopiracy alerts into DB.
    Call ONCE before hackathon demo — idempotent (skips existing).

    curl -X POST http://localhost:8000/api/alerts/seed
    """
    seeded = 0
    for data in DEMO_ALERTS:
        existing = await db.execute(
            select(BiopiacyAlert).where(BiopiacyAlert.id == data["id"])
        )
        if existing.scalar_one_or_none():
            continue   # already exists — skip

        alert = BiopiacyAlert(
            id=data["id"],
            patent_number=data["patent_number"],
            patent_title=data["patent_title"],
            applicant=data["applicant"],
            filing_country=data["filing_country"],
            filing_date=data["filing_date"],
            tkdl_match=data["tkdl_match"],
            similarity_score=data["similarity_score"],
            status=data["status"],
            action_deadline=data["action_deadline"],
            source_url=data["source_url"],
            is_read=data["is_read"],
            created_at=datetime.utcnow()
        )
        db.add(alert)
        seeded += 1

    await db.commit()
    return {"seeded": seeded, "message": f"{seeded} demo alerts added to database"}
