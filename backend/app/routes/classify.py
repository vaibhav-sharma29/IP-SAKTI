from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Classify"])

# ── Request / Response models ───────────────────────────────

class ClassifyRequest(BaseModel):
    description: str              # Product description in any language
    has_classical_ref: bool       # Is it from classical Ayurvedic text?
    has_novel_process: bool       # Novel extraction/process involved?
    has_health_claim: bool        # Does it make health/nutrition claims?
    is_topical: bool              # Applied on skin/hair? (cosmetic)
    language: str = "en"

class ClassifyResponse(BaseModel):
    category: str                 # e.g. "Classical Medicine"
    ip_posture: str               # What IP is possible
    regulatory_track: str         # Which ministry/act regulates it
    patent_possible: bool
    key_actions: list[str]        # Step-by-step recommended actions
    warning: str = ""             # Any conflict or risk detected

# ── Route ───────────────────────────────────────────────────

@router.post("/classify", response_model=ClassifyResponse)
async def classify_formulation(req: ClassifyRequest):
    """
    Formulation Classification Engine.

    Based on user's answers to 4 questions, classifies
    the Ayurvedic product and returns tailored IP guidance.

    Frontend Contract:
    - POST /api/classify
    - Body: { description, has_classical_ref, has_novel_process,
              has_health_claim, is_topical, language }
    - Response: { category, ip_posture, regulatory_track,
                  patent_possible, key_actions, warning }
    """

    # Classification logic — decision tree
    if req.has_classical_ref and not req.has_novel_process:
        return ClassifyResponse(
            category="Classical / Generic Medicine",
            ip_posture="Patent NOT possible on formula (Section 3(p), Patents Act 1970). Brand trademark possible. GI tag if region-specific.",
            regulatory_track="Drugs & Cosmetics Act — Schedule First",
            patent_possible=False,
            key_actions=[
                "Register brand as Trademark (Trademarks Act 1999)",
                "Check TKDL for prior art documentation",
                "Explore GI Tag if product is region-specific",
                "Protect manufacturing process as Trade Secret"
            ],
            warning="Formula is traditional knowledge — patent filing will be rejected and is wasteful."
        )

    elif req.has_novel_process:
        return ClassifyResponse(
            category="Proprietary / New Drug",
            ip_posture="Process patent possible (Section 2(1)(j)). Clinical evidence needed for New Drug approval.",
            regulatory_track="CDSCO — New Drug approval under D&C Act Rule 158",
            patent_possible=True,
            key_actions=[
                "File Process Patent immediately (Patents Act, Section 2(1)(j))",
                "Obtain NBA approval if using biodiversity resources (BD Act, Section 6)",
                "Conduct safety & efficacy trials as per NDCT Rules 2019",
                "Register trademark for brand"
            ],
            warning="NBA approval mandatory BEFORE patent filing if using any biological resource."
        )

    elif req.has_health_claim and not req.is_topical:
        return ClassifyResponse(
            category="Ayurveda-Aahar / Nutraceutical",
            ip_posture="Trademark possible. No drug claims allowed.",
            regulatory_track="FSSAI — Ayurveda Aahar Regulations",
            patent_possible=False,
            key_actions=[
                "Register under FSSAI as Nutraceutical",
                "Avoid drug/disease cure claims on label (DMRA Act)",
                "Use only permitted Ayurveda-Aahar ingredients list",
                "Trademark brand name"
            ],
            warning="Cannot claim 'cures', 'treats', or 'prevents' any disease under FSSAI regulations."
        )

    elif req.is_topical:
        return ClassifyResponse(
            category="Cosmetic / Herbal Cosmetic",
            ip_posture="Trademark possible. Design registration for packaging.",
            regulatory_track="Cosmetics Rules 2020 under D&C Act",
            patent_possible=False,
            key_actions=[
                "Obtain CDSCO Cosmetic Manufacturing License",
                "Ensure compliance with Cosmetics Rules 2020",
                "Trademark brand name",
                "Design registration for unique packaging"
            ],
            warning=""
        )

    else:
        return ClassifyResponse(
            category="Unclassified — More information needed",
            ip_posture="Cannot determine without more details.",
            regulatory_track="Please consult an AYUSH regulatory expert.",
            patent_possible=False,
            key_actions=["Provide more details about the product formulation"],
            warning=""
        )
