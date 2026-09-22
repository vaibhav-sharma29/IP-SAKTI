"""
Biopiracy Alerts — MongoDB
GET  /api/alerts
GET  /api/alerts/{id}
PATCH /api/alerts/{id}/read
POST /api/alerts/seed
"""

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import biopiracy_alerts

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
async def list_alerts(status: str = "open"):
    col = biopiracy_alerts()
    query = {} if status == "all" else {"status": status}
    cursor = col.find(query, {"_id": 0}).sort("similarity_score", -1)
    alerts = await cursor.to_list(length=50)
    return alerts


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: str):
    col = biopiracy_alerts()
    alert = await col.find_one({"id": alert_id}, {"_id": 0})
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.patch("/alerts/{alert_id}/read")
async def mark_read(alert_id: str):
    col = biopiracy_alerts()
    await col.update_one({"id": alert_id}, {"$set": {"is_read": True}})
    return {"success": True}


@router.post("/alerts/seed")
async def seed_demo_alerts():
    """Seed realistic demo alerts — run once before demo."""
    col = biopiracy_alerts()
    seeded = 0
    for data in DEMO_ALERTS:
        exists = await col.find_one({"id": data["id"]})
        if not exists:
            await col.insert_one(data)
            seeded += 1
    return {"seeded": seeded, "message": f"{seeded} demo alerts added"}
