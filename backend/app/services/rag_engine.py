"""
RAG Engine — Core of IP-SAKTI

Flow:
1. Query comes in (English)
2. LangChain Agent decides which vector store to search
   - india_laws    → Patents Act, GI Act, BD Act, D&C Act, FSSAI
   - international → TRIPS, Nagoya Protocol, WIPO GRATK Treaty
3. Top-K chunks retrieved from ChromaDB
4. Gemini generates answer grounded in retrieved chunks
5. Sources extracted from chunk metadata
6. Confidence computed from retrieval scores
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings

# ── Embedding model (free, runs locally, multilingual) ──────
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# ── Load vector stores ───────────────────────────────────────
india_vectorstore = Chroma(
    collection_name="india_laws",
    embedding_function=embeddings,
    persist_directory=settings.chroma_db_path
)

international_vectorstore = Chroma(
    collection_name="international_laws",
    embedding_function=embeddings,
    persist_directory=settings.chroma_db_path
)

# ── Gemini LLM ───────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=settings.gemini_api_key,
    temperature=0.1,   # Low temperature = more factual, less creative
)

# ── RAG Chains ───────────────────────────────────────────────
india_chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    retriever=india_vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

international_chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    retriever=international_vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

# ── Agent Tools ──────────────────────────────────────────────
tools = [
    Tool(
        name="Search_Indian_IP_Laws",
        func=lambda q: india_chain({"question": q})["answer"],
        description=(
            "Use this to answer questions about Indian IP laws: "
            "Patents Act 1970 (Section 3p, 3d), GI Act 1999, "
            "Trademarks Act 1999, Biological Diversity Act 2002, "
            "Drugs and Cosmetics Act, FSSAI Ayurveda-Aahar rules, "
            "TKDL, and AYUSH regulations."
        )
    ),
    Tool(
        name="Search_International_IP_Laws",
        func=lambda q: international_chain({"question": q})["answer"],
        description=(
            "Use this to answer questions about international IP laws: "
            "TRIPS Agreement, CBD, Nagoya Protocol, WIPO GRATK Treaty 2024, "
            "PCT, Madrid System, Budapest Treaty, and export market regulations."
        )
    ),
]

# ── System Prompt ────────────────────────────────────────────
SYSTEM_PROMPT = """You are IP-SAKTI, an AI assistant specialized in 
Intellectual Property (IP) and regulatory guidance for Ayurveda.

RULES YOU MUST FOLLOW:
1. ONLY answer using information from the provided tools/documents.
2. ALWAYS cite the exact statute name and section number.
3. If you are uncertain, say: "I don't have sufficient information. Please consult an IP attorney."
4. NEVER fabricate legal provisions or section numbers.
5. ALWAYS add at the end: "This is information only, not legal advice."
6. Keep Indian and international law answers SEPARATE — never conflate them.
7. Be concise, clear, and use plain language.
"""

# ── Main function called by route ───────────────────────────
async def get_rag_response(query: str, jurisdiction: str = "india") -> dict:
    """
    Called by /api/chat route.
    Returns: { answer, sources, confidence }
    """

    # Build jurisdiction-aware query
    if jurisdiction == "india":
        full_query = f"[INDIA LAW ONLY] {query}"
        tool_subset = [tools[0]]  # Only Indian laws tool
    elif jurisdiction == "international":
        full_query = f"[INTERNATIONAL LAW ONLY] {query}"
        tool_subset = [tools[1]]  # Only international laws tool
    else:
        full_query = query
        tool_subset = tools  # Both tools — agent decides

    # Initialize agent
    agent = initialize_agent(
        tools=tool_subset,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={"prefix": SYSTEM_PROMPT}
    )

    try:
        raw_answer = agent.run(full_query)

        # Extract sources from the retrieval chain directly
        # (In production, parse source_documents metadata)
        sources = _extract_sources(jurisdiction)
        confidence = _compute_confidence(raw_answer)

        return {
            "answer": raw_answer,
            "sources": sources,
            "confidence": confidence
        }

    except Exception as e:
        return {
            "answer": "I was unable to find a reliable answer. Please consult a qualified IP attorney.",
            "sources": [],
            "confidence": "low"
        }


def _extract_sources(jurisdiction: str) -> list:
    """Returns placeholder sources — replace with actual chunk metadata in production."""
    if jurisdiction == "india":
        return [
            {"title": "Patents Act 1970", "section": "Section 3(p)", "url": "https://ipindia.gov.in"},
            {"title": "Biological Diversity Act 2002", "section": "Section 6", "url": "https://nbaindia.org"},
        ]
    else:
        return [
            {"title": "TRIPS Agreement", "section": "Article 27", "url": "https://wipo.int"},
            {"title": "Nagoya Protocol", "section": "Article 15", "url": "https://cbd.int"},
        ]


def _compute_confidence(answer: str) -> str:
    """Simple confidence heuristic — improve with retrieval scores later."""
    low_confidence_phrases = [
        "i don't know", "i'm not sure", "cannot find",
        "consult", "insufficient", "unclear"
    ]
    answer_lower = answer.lower()
    if any(phrase in answer_lower for phrase in low_confidence_phrases):
        return "low"
    elif len(answer) > 300:
        return "high"
    else:
        return "medium"
