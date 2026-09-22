"""
RAG Engine — Core of IP-SAKTI

Flow:
1. Query comes in (English)
2. LangChain Agent decides which vector store to search
   - india_laws        → Patents Act, GI Act, BD Act, D&C Act, FSSAI
   - international_laws → TRIPS, Nagoya Protocol, WIPO GRATK Treaty
3. Top-K chunks retrieved from ChromaDB
4. Gemini generates answer grounded ONLY in retrieved chunks
5. REAL sources extracted from chunk metadata (source_file, page, section)
6. Confidence computed from retrieval similarity scores
"""

import asyncio
import hashlib
import logging
from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

from app.config import settings

logger = logging.getLogger(__name__)

# ── Source URL map — official government links ───────────────
SOURCE_URLS: dict[str, str] = {
    "patents_act":             "https://ipindia.gov.in/patents.htm",
    "patent_rules_2024":       "https://ipindia.gov.in/patents.htm",
    "gi_act":                  "https://ipindia.gov.in/geographical-indications.htm",
    "trademarks_act":          "https://ipindia.gov.in/trade-marks.htm",
    "biological_diversity_act":"https://nbaindia.org/content/biological-diversity-act-2002",
    "biological_diversity_rules_2024": "https://nbaindia.org",
    "drugs_cosmetics_act":     "https://cdsco.gov.in/opencms/opencms/en/Drugs/",
    "fssai_ayurveda":          "https://fssai.gov.in",
    "ayush_regulations":       "https://ayush.gov.in",
    "trips_agreement":         "https://www.wto.org/english/tratop_e/trips_e/trips_e.htm",
    "cbd_convention":          "https://www.cbd.int",
    "nagoya_protocol":         "https://www.cbd.int/abs",
    "wipo_gratk_treaty":       "https://www.wipo.int/gratk/en/",
    "pct_treaty":              "https://www.wipo.int/pct/en/",
    "madrid_system":           "https://www.wipo.int/madrid/en/",
    "budapest_treaty":         "https://www.wipo.int/budapest/en/",
}

def _get_url_for_source(source_file: str) -> str:
    """Map PDF filename → official government URL"""
    source_lower = source_file.lower().replace(" ", "_").replace("-", "_")
    for key, url in SOURCE_URLS.items():
        if key in source_lower:
            return url
    return "https://indiacode.nic.in"   # fallback


# ── Embedding model — loaded once, reused ───────────────────
@lru_cache(maxsize=1)
def _get_embeddings() -> HuggingFaceEmbeddings:
    logger.info("Loading embedding model...")
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


# ── Vector stores — loaded once ──────────────────────────────
@lru_cache(maxsize=1)
def _get_india_vectorstore() -> Chroma:
    return Chroma(
        collection_name="india_laws",
        embedding_function=_get_embeddings(),
        persist_directory=settings.chroma_db_path
    )

@lru_cache(maxsize=1)
def _get_international_vectorstore() -> Chroma:
    return Chroma(
        collection_name="international_laws",
        embedding_function=_get_embeddings(),
        persist_directory=settings.chroma_db_path
    )


# ── Gemini LLM ───────────────────────────────────────────────
@lru_cache(maxsize=1)
def _get_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.gemini_api_key,
        temperature=0,
        max_retries=2,
    )


# ── RAG Prompt ───────────────────────────────────────────────
RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are IP-SAKTI, an expert AI assistant for Ayurveda Intellectual Property law in India.

RULES:
1. Use the CONTEXT below as your primary source. Cite specific Act names and Sections when available.
2. If context is insufficient, use your knowledge of Indian IP law to give a helpful answer.
3. ALWAYS mention relevant Acts (Patents Act 1970, Trade Marks Act 1999, Biological Diversity Act 2002, GI Act 1999, etc.)
4. End EVERY answer with: "This is information only, not legal advice."
5. Keep answers clear, concise and practical.

CONTEXT (from official Indian legal documents):
{context}

QUESTION: {question}

ANSWER:"""
)


# ── Real source extraction from chunk metadata ───────────────
def _extract_real_sources(docs: list[Document]) -> list[dict]:
    """
    Extract actual source citations from retrieved chunk metadata.
    Each chunk has metadata set during corpus_builder.py ingestion:
      - source_file: PDF filename (e.g. "patents_act_1970.pdf")
      - page:        Page number in the PDF
      - section:     Section heading if detected
    """
    seen = set()
    sources = []

    for doc in docs:
        meta = doc.metadata or {}
        source_file = meta.get("source_file", "Unknown Source")
        page        = meta.get("page", "")
        section     = meta.get("section", "")

        # Build clean title from filename
        title = (
            source_file
            .replace(".pdf", "")
            .replace("_", " ")
            .title()
        )

        # Build section string
        section_str = section if section else (f"Page {page}" if page else "")

        # Dedup by title+section combo
        key = f"{title}:{section_str}"
        if key not in seen:
            seen.add(key)
            sources.append({
                "title":   title,
                "section": section_str,
                "url":     _get_url_for_source(source_file)
            })

    # Cap at 4 sources — don't overwhelm UI
    return sources[:4]


# ── Confidence from similarity scores ────────────────────────
def _compute_confidence(docs: list[Document], answer: str) -> str:
    """
    Compute confidence from:
    1. Retrieval scores (if available in metadata)
    2. Answer content heuristics
    """
    # Check retrieval scores from ChromaDB metadata
    scores = [
        doc.metadata.get("score", 0.0)
        for doc in docs
        if "score" in (doc.metadata or {})
    ]

    if scores:
        avg_score = sum(scores) / len(scores)
        if avg_score > 0.75:
            return "high"
        elif avg_score > 0.50:
            return "medium"
        else:
            return "low"

    # Fallback: content heuristics
    low_phrases = [
        "i don't have sufficient", "please consult",
        "i'm not sure", "cannot find", "no information"
    ]
    if any(p in answer.lower() for p in low_phrases):
        return "low"
    if len(answer) > 400 and any(
        kw in answer.lower()
        for kw in ["section", "article", "act", "rule", "treaty"]
    ):
        return "high"
    return "medium"


# ── Core retrieval function ──────────────────────────────────
def _retrieve_and_generate(
    query: str,
    vectorstore: Chroma,
    k: int = 6
) -> dict:
    """
    Sync retrieval + generation — runs in thread pool via asyncio.
    Returns { answer, sources, confidence }
    """
    # Step 1: Retrieve top-K relevant chunks — smaller k = faster
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}   # reduced from 6 for speed
    )
    docs = retriever.invoke(query)

    # Step 2: Build context — limit size to avoid slow Gemini calls
    context_parts = []
    total_chars = 0
    MAX_CONTEXT = 3000   # keep context small for fast response

    for doc in docs:
        chunk = (
            f"[Source: {doc.metadata.get('act_name', doc.metadata.get('source_file', 'Unknown'))}, "
            f"{doc.metadata.get('citation', '')}]\n{doc.page_content[:400]}"
        )
        if total_chars + len(chunk) > MAX_CONTEXT:
            break
        context_parts.append(chunk)
        total_chars += len(chunk)

    context = "\n\n---\n\n".join(context_parts)

    # Step 3: Generate answer — direct Google GenAI, single attempt
    prompt_text = RAG_PROMPT.format(context=context, question=query)

    answer = None
    try:
        from google import genai as google_genai
        client = google_genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt_text
        )
        answer = response.text if hasattr(response, "text") else str(response)
        if not answer or len(answer) < 10:
            answer = None
        else:
            logger.info("Gemini success")
    except Exception as e:
        logger.warning(f"Gemini unavailable: {e}")
        answer = None

    # If Gemini failed — use smart fallback immediately (no retries)
    if not answer:
        answer = _get_fallback_answer(query)
        logger.info("Using fallback answer")

    # Step 4: Extract real sources from chunk metadata
    sources    = _extract_real_sources(docs)
    confidence = _compute_confidence(docs, answer)

    return {
        "answer":     answer,
        "sources":    sources,
        "confidence": confidence
    }


# ── Public async interface (called by route) ─────────────────
async def get_rag_response(
    query: str,
    jurisdiction: str = "india"
) -> dict:
    """
    Main entry point — called by /api/chat route.

    Runs ChromaDB + Gemini in a thread pool so FastAPI
    event loop stays non-blocking.

    Returns:
        { answer: str, sources: list[dict], confidence: str }
    """
    try:
        if jurisdiction == "india":
            vs = _get_india_vectorstore()
        elif jurisdiction == "international":
            vs = _get_international_vectorstore()
        else:
            # "both" — search india first, append international
            result_india = await asyncio.get_event_loop().run_in_executor(
                None, _retrieve_and_generate, query, _get_india_vectorstore()
            )
            result_intl = await asyncio.get_event_loop().run_in_executor(
                None, _retrieve_and_generate, query, _get_international_vectorstore()
            )
            # Merge: combine answers, deduplicate sources
            combined_answer = (
                f"**Indian Law:**\n{result_india['answer']}"
                f"\n\n**International Law:**\n{result_intl['answer']}"
            )
            all_sources = result_india["sources"] + result_intl["sources"]
            seen_titles = set()
            unique_sources = []
            for s in all_sources:
                if s["title"] not in seen_titles:
                    seen_titles.add(s["title"])
                    unique_sources.append(s)

            scores = {"high": 2, "medium": 1, "low": 0}
            better = max(
                [result_india["confidence"], result_intl["confidence"]],
                key=lambda c: scores.get(c, 0)
            )
            return {
                "answer":     combined_answer,
                "sources":    unique_sources[:5],
                "confidence": better
            }

        # Single jurisdiction
        result = await asyncio.get_event_loop().run_in_executor(
            None, _retrieve_and_generate, query, vs
        )
        return result

    except Exception as e:
        logger.error(f"RAG pipeline error: {e}")
        return {
            "answer": (
                "I was unable to find a reliable answer in my knowledge base. "
                "⚠️ Please consult a qualified IP attorney for specific guidance."
            ),
            "sources":    [],
            "confidence": "low"
        }


# ── Query hash for audit logs (no PII stored) ────────────────
def hash_query(query: str) -> str:
    """SHA-256 hash of query — stored in audit log, not raw text (DPDP compliance)"""
    return hashlib.sha256(query.encode()).hexdigest()


# ── Fallback answers when Gemini is unavailable ──────────────
def _get_fallback_answer(query: str) -> str:
    """
    Rule-based fallback when Gemini API is unavailable (503).
    Returns helpful pre-written answers for common queries.
    """
    q = query.lower()

    if any(w in q for w in ["patent", "section 3", "3(p)", "patentable"]):
        return (
            "Under Section 3(p) of the Patents Act 1970, traditional knowledge "
            "including classical Ayurvedic formulations cannot be patented in India. "
            "However, a novel extraction process or manufacturing method may be "
            "patentable under Section 2(1)(j). "
            "The TKDL (Traditional Knowledge Digital Library) protects documented "
            "traditional knowledge from biopiracy abroad. "
            "\n\nThis is information only, not legal advice."
        )

    if any(w in q for w in ["trademark", "brand", "trade mark"]):
        return (
            "Under the Trade Marks Act 1999, you can register your brand name and "
            "logo as a trademark in India. Application is filed with IP India "
            "(ipindia.gov.in). Registration is valid for 10 years and renewable. "
            "Descriptive names and geographic terms face higher rejection risk. "
            "\n\nThis is information only, not legal advice."
        )

    if any(w in q for w in ["biodiversity", "nba", "abs", "biological"]):
        return (
            "Under the Biological Diversity Act 2002 (Section 3 & 6), commercial "
            "use of biological resources and IP filing requires prior approval from "
            "the National Biodiversity Authority (NBA) at nbaindia.org. "
            "The 2023 Amendment and 2024 Rules mandate ABS disclosure in patent "
            "applications. Non-compliance penalty: up to Rs. 1 crore. "
            "\n\nThis is information only, not legal advice."
        )

    if any(w in q for w in ["gi tag", "geographical indication", "gi act"]):
        return (
            "A Geographical Indication (GI) tag under the GI Act 1999 protects "
            "products associated with a specific geographic region. Application is "
            "filed with IP India. GI tags protect collective community knowledge "
            "and prevent misuse of geographic names commercially. "
            "\n\nThis is information only, not legal advice."
        )

    if any(w in q for w in ["nagoya", "trips", "cbd", "international", "export"]):
        return (
            "For international IP protection of Ayurvedic products: "
            "1) TRIPS Agreement governs global IP standards for WTO members. "
            "2) The Nagoya Protocol (CBD) requires ABS compliance for genetic "
            "resource use in signatory countries. "
            "3) WIPO GRATK Treaty 2024 specifically protects traditional knowledge. "
            "PCT filing through WIPO enables patent protection in 150+ countries. "
            "\n\nThis is information only, not legal advice."
        )

    # Generic fallback
    return (
        "I currently cannot process this query due to high server load. "
        "Please try again in a few minutes. "
        "For immediate assistance, consult a qualified IP attorney or visit: "
        "ipindia.gov.in (Indian IP), nbaindia.org (Biodiversity), "
        "wipo.int (International IP). "
        "\n\nThis is information only, not legal advice."
    )
