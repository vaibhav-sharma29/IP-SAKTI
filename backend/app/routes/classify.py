"""
Formulation Classification Engine

Two-layer approach:
1. AI Layer: Gemini reads user's product description →
             auto-detects answers to 4 questions
2. Rule Layer: Deterministic decision tree →
              gives exact IP guidance

Why rule-based for final output:
Legal accuracy requires determinism.
AI is used only for input understanding,
not for legal conclusions.
"""

import logging
from fastapi import APIRouter
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Classify"])


# ── Models ───────────────────────────────────────────────────

class ClassifyRequest(BaseModel):
    description:       str
    has_classical_ref: bool
    has_novel_process: bool
    has_health_claim:  bool
    is_topical:        bool
    language:          str = "en"

class AutoDetectRequest(BaseModel):
    """
    AI auto-detect endpoint — user gives description,
    AI pre-fills the 4 yes/no answers.
    Frontend uses this to pre-populate the wizard.
    """
    description: str

class AutoDetectResponse(BaseModel):
    has_classical_ref: bool
    has_novel_process: bool
    has_health_claim:  bool
    is_topical:        bool
    reasoning:         str   # Why AI made these choices

class ClassifyResponse(BaseModel):
    category:          str
    ip_posture:        str
    regulatory_track:  str
    patent_possible:   bool
    key_actions:       list[str]
    warning:           str = ""
    abs_required:      bool = False   # NEW: NBA/ABS approval needed?
    abs_checklist:     list[str] = [] # NEW: ABS steps if required


# ── AI Auto-Detect ───────────────────────────────────────────

@router.post("/classify/auto-detect", response_model=AutoDetectResponse)
async def auto_detect(req: AutoDetectRequest):
    """
    AI reads product description and pre-fills classifier questions.
    Frontend calls this first — user can override the AI's answers.

    Example:
      Input: "Ashwagandha root extract using novel CO2 supercritical process"
      Output: has_classical_ref=True, has_novel_process=True, ...
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            google_api_key=settings.gemini_api_key,
            temperature=0
        )

        prompt = f"""You are an Ayurveda IP expert. Analyze this product description and answer 4 questions.

Product Description: "{req.description}"

Answer each question with ONLY true or false:

Q1 has_classical_ref: Is this formula/ingredient mentioned in classical Ayurvedic texts 
   (Charaka Samhita, Sushruta Samhita, Ashtanga Hridayam, Bhavaprakasha, etc.)?
   → true if ingredient like Ashwagandha, Neem, Turmeric, Brahmi etc. is classical

Q2 has_novel_process: Does it involve a novel/new extraction, manufacturing, or 
   formulation process not documented in classical texts?
   → true if keywords like "novel", "extract", "CO2", "nanoparticle", "standardized" etc.

Q3 has_health_claim: Does it make health, nutrition, or therapeutic claims?
   → true if it mentions "immunity", "cognitive", "anti-inflammatory", "supplement" etc.

Q4 is_topical: Is it applied on skin or hair (not consumed internally)?
   → true if cream, oil, serum, shampoo, face pack etc.

Also give a brief reasoning (1-2 sentences).

Respond in EXACTLY this format:
has_classical_ref: true/false
has_novel_process: true/false
has_health_claim: true/false
is_topical: true/false
reasoning: [your reasoning here]"""

        response = llm.invoke(prompt)
        text = response.content if hasattr(response, "content") else str(response)
        if isinstance(text, list):
            text = " ".join(str(p) for p in text)

        # Parse response
        lines = text.strip().split("\n")
        result = {}
        reasoning = ""
        for line in lines:
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower()
                val = val.strip().lower()
                if key == "reasoning":
                    reasoning = val.strip()
                elif key in ["has_classical_ref", "has_novel_process",
                             "has_health_claim", "is_topical"]:
                    result[key] = val.startswith("true")

        return AutoDetectResponse(
            has_classical_ref=result.get("has_classical_ref", False),
            has_novel_process=result.get("has_novel_process", False),
            has_health_claim=result.get("has_health_claim", True),
            is_topical=result.get("is_topical", False),
            reasoning=reasoning or "Based on description analysis."
        )

    except Exception as e:
        logger.warning(f"Auto-detect failed: {e}, returning defaults")
        # Graceful fallback — return sensible defaults
        return AutoDetectResponse(
            has_classical_ref=False,
            has_novel_process=False,
            has_health_claim=True,
            is_topical=False,
            reasoning="Auto-detection unavailable. Please answer questions manually."
        )


# ── Main Classifier ──────────────────────────────────────────

@router.post("/classify", response_model=ClassifyResponse)
def classify_formulation(req: ClassifyRequest):
    """
    Deterministic rule-based classifier.
    Takes 4 boolean answers → returns exact IP guidance.
    Rule-based is intentional for legal accuracy.
    """

    # Shared ABS checklist — shown when biodiversity resources used
    ABS_CHECKLIST = [
        "Check if ingredient is a biological resource under Biodiversity Act 2002",
        "Obtain Prior Informed Consent (PIC) from National Biodiversity Authority (NBA)",
        "Sign Access and Benefit Sharing (ABS) agreement",
        "File ABS disclosure with patent application (mandatory post 2024 Rules)",
        "Register with State Biodiversity Board if sourcing locally",
        "For international use: comply with Nagoya Protocol disclosure requirements",
    ]

    # ── Classical + No Novel Process ─────────────────────────
    if req.has_classical_ref and not req.has_novel_process:
        return ClassifyResponse(
            category="Classical / Generic Medicine",
            ip_posture=(
                "Patent on formula is BARRED under Section 3(p) of Patents Act 1970 "
                "— traditional knowledge cannot be patented. However, brand protection "
                "via Trademark and GI Tag (if region-specific) are available."
            ),
            regulatory_track="Drugs & Cosmetics Act 1940 — Schedule First (classical formulations)",
            patent_possible=False,
            key_actions=[
                "Register brand name as Trademark (Trade Marks Act 1999, Section 18)",
                "Check TKDL (tkdl.res.in) to confirm prior art documentation",
                "Apply for GI Tag if product is region-specific (GI Act 1999)",
                "Protect proprietary manufacturing process as Trade Secret",
                "File Trademark for logo/packaging design (Designs Act 2000)",
            ],
            warning=(
                "Formula is traditional knowledge — Section 3(p) bars patentability. "
                "Any patent filing will be rejected and filing fees wasted."
            ),
            abs_required=req.has_classical_ref,
            abs_checklist=ABS_CHECKLIST if req.has_classical_ref else []
        )

    # ── Novel Process (with or without classical ref) ────────
    elif req.has_novel_process:
        return ClassifyResponse(
            category="Proprietary Medicine / New Drug with Novel Process",
            ip_posture=(
                "Process patent IS possible under Section 2(1)(j) of Patents Act 1970 "
                "for the novel extraction/manufacturing process. The underlying formula "
                "may still be barred under Section 3(p) if classical, but the process itself "
                "is patentable. New Drug approval required under D&C Act Rule 158."
            ),
            regulatory_track="CDSCO — New Drug approval under Drugs & Cosmetics Act, Rule 158 / NDCT Rules 2019",
            patent_possible=True,
            key_actions=[
                "File Process Patent immediately (Patents Act 1970, Section 2(1)(j)) — priority date matters",
                "Obtain NBA approval BEFORE patent filing (Biological Diversity Act 2002, Section 6)",
                "Conduct Phase I/II safety & efficacy trials as per NDCT Rules 2019",
                "File New Drug Application with CDSCO (Form 44)",
                "Register Trademark for brand name (Trade Marks Act 1999)",
                "Consider PCT filing for international protection (within 12 months of Indian filing)",
            ],
            warning=(
                "NBA approval is MANDATORY before filing patent if any biological resource "
                "is used. Post-2024 Rules: ABS disclosure in patent application is legally required."
            ),
            abs_required=True,
            abs_checklist=ABS_CHECKLIST
        )

    # ── Health Claims, Not Topical → Nutraceutical ───────────
    elif req.has_health_claim and not req.is_topical:
        return ClassifyResponse(
            category="Ayurveda-Aahar / Nutraceutical",
            ip_posture=(
                "Trademark for brand is possible. No patent on formula. "
                "FSSAI regulates health claims — only permitted claims from "
                "FSSAI's Ayurveda-Aahar approved list can be used on label."
            ),
            regulatory_track="FSSAI — Ayurveda-Aahar Regulations 2022 + Drugs & Magic Remedies Act 1954",
            patent_possible=False,
            key_actions=[
                "Register as Nutraceutical under FSSAI (Food Safety & Standards Act 2006)",
                "Use ONLY permitted Ayurveda-Aahar ingredient list (FSSAI Schedule)",
                "Avoid 'cures', 'treats', 'prevents' any disease on label (DMRA Act 1954)",
                "Permitted claims: 'supports', 'promotes', 'helps maintain' (FSSAI guidelines)",
                "Register Trademark for brand name",
                "Check if any ingredient needs NBA approval",
            ],
            warning=(
                "CRITICAL: Cannot use drug/disease claims (DMRA Act). "
                "Labels must comply with Food Safety & Standards (Labelling) Regulations 2011."
            ),
            abs_required=False,
            abs_checklist=[]
        )

    # ── Topical → Cosmetic ───────────────────────────────────
    elif req.is_topical:
        return ClassifyResponse(
            category="Herbal Cosmetic / Ayurvedic Cosmetic",
            ip_posture=(
                "Trademark for brand is possible. Design registration for unique packaging. "
                "No patent on classical formula. Novel formulation process may be patentable."
            ),
            regulatory_track="Cosmetics Rules 2020 under Drugs & Cosmetics Act 1940 — CDSCO cosmetics division",
            patent_possible=req.has_novel_process,
            key_actions=[
                "Obtain Cosmetic Manufacturing License (Cosmetics Rules 2020, Rule 7)",
                "Ensure all ingredients are in CDSCO permitted list for cosmetics",
                "Register Trademark for brand name",
                "Design registration for unique packaging (Designs Act 2000)",
                "Label must include ingredient list (INCI names) and shelf life",
                "No therapeutic claims allowed on cosmetic labels",
            ],
            warning=(
                "Cannot claim therapeutic benefits on cosmetic product. "
                "If therapeutic claims are made, product becomes a 'drug' "
                "and requires full drug approval."
            ),
            abs_required=False,
            abs_checklist=[]
        )

    # ── Fallback ─────────────────────────────────────────────
    else:
        return ClassifyResponse(
            category="Phytopharmaceutical / Unclassified",
            ip_posture="Cannot determine IP position without more details.",
            regulatory_track="Consult AYUSH Ministry or CDSCO for classification",
            patent_possible=False,
            key_actions=[
                "Contact AYUSH Ministry helpdesk for product classification guidance",
                "Consult a registered IP attorney for specific advice",
            ],
            warning="",
            abs_required=False,
            abs_checklist=[]
        )
