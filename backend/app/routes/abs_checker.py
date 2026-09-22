"""
ABS Compliance Checker — GET /api/abs/checklist
POST /api/abs/check

Access and Benefit Sharing (ABS) compliance
under Biological Diversity Act 2002 (amended 2023)
and Biological Diversity Rules 2024.

PS requirement: "ABS-compliance helper"
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["ABS Compliance"])


class ABSCheckRequest(BaseModel):
    uses_biological_resource: bool   # Plant, microbe, animal derived?
    is_commercial_use:        bool   # Selling the product?
    involves_research:        bool   # Research/patent filing?
    is_foreign_entity:        bool   # Foreign company/person involved?
    source_state:             str = ""  # Which Indian state sourcing from


class ABSCheckResponse(BaseModel):
    nba_approval_required:    bool
    risk_level:               str        # "high" | "medium" | "low"
    applicable_sections:      list[str]  # Exact law sections
    required_steps:           list[dict] # {step, description, link}
    timeline_estimate:        str
    penalty_if_ignored:       str


@router.post("/abs/check", response_model=ABSCheckResponse)
def check_abs_compliance(req: ABSCheckRequest):
    """
    Checks ABS compliance requirements based on product/activity profile.
    Returns exact steps, sections, and consequences.
    """

    steps = []
    sections = []
    risk = "low"

    # ── Core check ───────────────────────────────────────────
    if req.uses_biological_resource and req.is_commercial_use:
        risk = "high"
        sections = [
            "Biological Diversity Act 2002, Section 3 — Prior approval for commercial use",
            "Biological Diversity Act 2002, Section 6 — ABS approval before IP filing",
            "Biological Diversity Rules 2024, Rule 14 — Application procedure",
            "Nagoya Protocol, Article 15 — Access to Genetic Resources",
        ]
        steps = [
            {
                "step": "1. Check ENVIS Portal",
                "description": "Verify if your biological resource is in the notified list",
                "link": "http://nbaindia.org/content/notification",
                "mandatory": True
            },
            {
                "step": "2. Apply to NBA for Prior Approval",
                "description": "Submit Form I to National Biodiversity Authority BEFORE commercial use",
                "link": "https://nbaindia.org/content/apply-approval",
                "mandatory": True
            },
            {
                "step": "3. Sign ABS Agreement",
                "description": "Execute Mutually Agreed Terms (MAT) with NBA for benefit sharing",
                "link": "https://nbaindia.org",
                "mandatory": True
            },
            {
                "step": "4. Register with State Biodiversity Board",
                "description": "If sourcing from a specific state, register with that State Biodiversity Board",
                "link": "https://nbaindia.org/content/state-biodiversity-boards",
                "mandatory": req.source_state != ""
            },
        ]

        if req.involves_research:
            sections.append("Biological Diversity Act 2002, Section 4 — Research on biological resources")
            steps.append({
                "step": "5. ABS Disclosure in Patent",
                "description": "Disclose ABS compliance in patent application (mandatory post-2024 Rules)",
                "link": "https://ipindia.gov.in",
                "mandatory": True
            })

        if req.is_foreign_entity:
            sections.append("Biological Diversity Act 2002, Section 3 — Foreign entities need special approval")
            sections.append("Nagoya Protocol, Article 6 — Access by foreign nationals")
            steps.append({
                "step": "6. Foreign Entity Prior Approval",
                "description": "Foreign companies need separate NBA approval under Section 3",
                "link": "https://nbaindia.org",
                "mandatory": True
            })

        timeline = "3-6 months for NBA approval (apply early)"
        penalty = (
            "Penalty for non-compliance: Up to ₹1 crore fine + "
            "imprisonment up to 3 years (Section 55, BD Act). "
            "Patent may be revoked if ABS not disclosed."
        )

    elif req.uses_biological_resource and req.involves_research:
        risk = "medium"
        sections = [
            "Biological Diversity Act 2002, Section 4 — Approval for research",
            "Biological Diversity Rules 2024, Rule 14",
        ]
        steps = [
            {
                "step": "1. Apply to NBA for Research Approval",
                "description": "Academic/research use requires NBA approval under Section 4",
                "link": "https://nbaindia.org",
                "mandatory": True
            }
        ]
        timeline = "1-3 months for research approval"
        penalty = "Penalty: Up to ₹10 lakh fine for unauthorized research use"

    else:
        risk = "low"
        sections = ["Biological Diversity Act 2002 — No approval needed for personal/local use"]
        steps = [
            {
                "step": "1. Confirm non-commercial use",
                "description": "Local communities and Vaids/Hakims are exempt under Section 41",
                "link": "https://nbaindia.org",
                "mandatory": False
            }
        ]
        timeline = "No approval required"
        penalty = "No penalty for personal/local traditional use"

    return ABSCheckResponse(
        nba_approval_required=(risk in ["high", "medium"]),
        risk_level=risk,
        applicable_sections=sections,
        required_steps=steps,
        timeline_estimate=timeline,
        penalty_if_ignored=penalty
    )


@router.get("/abs/checklist")
def get_abs_quick_checklist():
    """
    Quick reference checklist for ABS compliance.
    Frontend shows this as a static guide.
    """
    return {
        "title": "ABS Compliance Quick Checklist",
        "law": "Biological Diversity Act 2002 + 2024 Rules",
        "checklist": [
            {
                "question": "Is your product derived from a biological resource (plant/microbe/animal)?",
                "if_yes": "NBA approval may be required",
                "section": "BD Act, Section 2(c)"
            },
            {
                "question": "Are you using it for commercial purposes?",
                "if_yes": "NBA Prior Approval mandatory (Section 3)",
                "section": "BD Act, Section 3"
            },
            {
                "question": "Are you filing a patent?",
                "if_yes": "ABS disclosure in patent application mandatory (post-2024 Rules)",
                "section": "BD Act, Section 6 + Patent Rules 2024"
            },
            {
                "question": "Is a foreign company involved?",
                "if_yes": "Separate approval under Section 3 required",
                "section": "BD Act, Section 3 + Nagoya Protocol"
            },
            {
                "question": "Selling internationally?",
                "if_yes": "Nagoya Protocol compliance in buyer's country required",
                "section": "Nagoya Protocol, Articles 15-16"
            },
        ],
        "nba_contact": {
            "website": "https://nbaindia.org",
            "email": "nba-envis@nic.in",
            "phone": "044-22200963"
        }
    }
