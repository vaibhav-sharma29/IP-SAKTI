"""
Corpus Builder — Run ONCE before hackathon to build ChromaDB.

Steps:
1. Place PDFs in backend/data/raw_pdfs/india/ and /international/
2. Run: python -m app.services.corpus_builder
3. ChromaDB built at ./chroma_db/
"""

import os
import re
import glob
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

PDF_DIR            = "./data/raw_pdfs"
CHROMA_DB_PATH     = "./chroma_db"
INDIA_PDF_DIR      = os.path.join(PDF_DIR, "india")
INTERNATIONAL_PDF_DIR = os.path.join(PDF_DIR, "international")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " "]
)

# ── Section detection patterns ───────────────────────────────
SECTION_PATTERNS = [
    # Indian Acts: "Section 3(p)", "Sec. 3", "S. 3"
    r'[Ss]ection\s+\d+[A-Za-z]?(?:\([a-z0-9]+\))*',
    r'[Ss]ec\.\s*\d+[A-Za-z]?',
    # Rules: "Rule 28", "Rule 131"
    r'[Rr]ule\s+\d+[A-Za-z]?',
    # Articles (international treaties): "Article 27", "Art. 15"
    r'[Aa]rticle\s+\d+[A-Za-z]?(?:\([a-z0-9]+\))*',
    r'[Aa]rt\.\s*\d+',
    # Clauses: "Clause 4(b)"
    r'[Cc]lause\s+\d+[A-Za-z]?(?:\([a-z0-9]+\))*',
    # Schedule: "Schedule I", "First Schedule"
    r'(?:First|Second|Third|Fourth|Fifth|Sixth)?\s*[Ss]chedule\s*[IVXivx]*',
    # Chapter: "Chapter III", "CHAPTER 2"
    r'[Cc][Hh][Aa][Pp][Tt][Ee][Rr]\s+[IVXivx\d]+',
]

def _extract_section(text: str) -> str:
    """
    Extract the most relevant section/article reference from chunk text.
    Returns the first match found, or empty string.
    """
    for pattern in SECTION_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            # Return first match, cleaned up
            return matches[0].strip()
    return ""


def _get_act_name(source_file: str) -> str:
    """Map filename to clean act name for citations."""
    mapping = {
        "patents_act":              "Patents Act 1970",
        "trademarks_act":           "Trade Marks Act 1999",
        "gi_act":                   "Geographical Indications Act 1999",
        "biological_diversity":     "Biological Diversity Act 2002",
        "drugs_cosmetics":          "Drugs & Cosmetics Act 1940",
        "fssai":                    "FSSAI Regulations",
        "ayush":                    "AYUSH Regulations",
        "trips":                    "TRIPS Agreement",
        "nagoya":                   "Nagoya Protocol",
        "cbd":                      "Convention on Biological Diversity",
        "wipo_gratk":               "WIPO GRATK Treaty 2024",
        "pct":                      "PCT Treaty",
        "madrid":                   "Madrid System",
    }
    lower = source_file.lower().replace("-", "_").replace(" ", "_")
    for key, name in mapping.items():
        if key in lower:
            return name
    return source_file.replace(".pdf", "").replace("_", " ").title()


def load_and_split_pdfs(pdf_dir: str) -> list:
    """Load PDFs, split into chunks, extract section metadata."""
    all_chunks = []
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))

    if not pdf_files:
        print(f"  No PDFs found in {pdf_dir}")
        return []

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        act_name = _get_act_name(filename)
        print(f"  Loading: {filename} → {act_name}")

        loader = PyMuPDFLoader(pdf_path)
        pages = loader.load()
        chunks = splitter.split_documents(pages)

        for chunk in chunks:
            # Extract section reference from chunk text
            section = _extract_section(chunk.page_content)
            page_num = chunk.metadata.get("page", 0)

            # Build rich metadata for source citations
            chunk.metadata.update({
                "source_file": filename,
                "act_name":    act_name,
                "section":     section,
                "page":        page_num,
                # Citation string: "Patents Act 1970, Section 3(p), Page 10"
                "citation": (
                    f"{act_name}, {section}" if section
                    else f"{act_name}, Page {page_num + 1}"
                )
            })

        all_chunks.extend(chunks)
        print(f"    → {len(chunks)} chunks")

    return all_chunks


def build_vectorstore(chunks: list, collection_name: str):
    if not chunks:
        print(f"  Skipping {collection_name} — no chunks")
        return

    print(f"\nBuilding ChromaDB: {collection_name} ({len(chunks)} chunks)...")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=CHROMA_DB_PATH
    )
    print(f"Done — {CHROMA_DB_PATH}")


if __name__ == "__main__":
    print("=" * 50)
    print("IP-SAKTI Corpus Builder")
    print("=" * 50)

    print("\n[1/2] Indian Laws...")
    india_chunks = load_and_split_pdfs(INDIA_PDF_DIR)
    build_vectorstore(india_chunks, "india_laws")

    print("\n[2/2] International Laws...")
    intl_chunks = load_and_split_pdfs(INTERNATIONAL_PDF_DIR)
    build_vectorstore(intl_chunks, "international_laws")

    # Show section detection stats
    india_with_sections = sum(1 for c in india_chunks if c.metadata.get("section"))
    intl_with_sections  = sum(1 for c in intl_chunks  if c.metadata.get("section"))

    print("\n" + "=" * 50)
    print(f"India:         {len(india_chunks)} chunks, {india_with_sections} with section refs")
    print(f"International: {len(intl_chunks)} chunks, {intl_with_sections} with section refs")
    print("Corpus build complete!")
