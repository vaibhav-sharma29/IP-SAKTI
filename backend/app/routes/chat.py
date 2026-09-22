from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_engine import get_rag_response
from app.services.translation import translate_to_english, translate_to_hindi

router = APIRouter(tags=["Chat"])

# ── Request / Response models (shared contract with frontend) ──

class ChatRequest(BaseModel):
    query: str                        # User ka sawaal
    language: str = "en"             # "en" or "hi"
    jurisdiction: str = "india"      # "india" or "international"
    session_id: str = "default"      # For future chat history

class Source(BaseModel):
    title: str                        # e.g. "Patents Act 1970"
    section: str                      # e.g. "Section 3(p)"
    url: str = ""                     # Link to official doc

class ChatResponse(BaseModel):
    answer: str                       # Final answer text
    sources: list[Source]             # List of cited sources
    confidence: str                   # "high" | "medium" | "low"
    disclaimer: str                   # Legal disclaimer (always shown)
    jurisdiction: str                 # Echo back jurisdiction used

# ── Route ──────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Main chat endpoint.

    Flow:
    1. If Hindi → translate to English
    2. Run RAG pipeline (LangChain Agent)
    3. If Hindi → translate answer back to Hindi
    4. Return structured response with citations

    Frontend Contract:
    - POST /api/chat
    - Body: { query, language, jurisdiction, session_id }
    - Response: { answer, sources, confidence, disclaimer, jurisdiction }
    """
    try:
        # Step 1: Translate if Hindi
        english_query = req.query
        if req.language == "hi":
            english_query = await translate_to_english(req.query)

        # Step 2: RAG pipeline
        result = await get_rag_response(
            query=english_query,
            jurisdiction=req.jurisdiction
        )

        # Step 3: Translate answer back if Hindi requested
        final_answer = result["answer"]
        if req.language == "hi":
            final_answer = await translate_to_hindi(result["answer"])

        return ChatResponse(
            answer=final_answer,
            sources=result["sources"],
            confidence=result["confidence"],
            disclaimer="This is information only, not legal advice. Consult a qualified IP attorney for specific cases.",
            jurisdiction=req.jurisdiction
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
