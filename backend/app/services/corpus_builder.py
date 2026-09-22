"""
Corpus Builder — Run this ONCE before the hackathon to build ChromaDB.

Steps:
1. Place all downloaded PDFs in backend/data/raw_pdfs/
2. Run: python -m app.services.corpus_builder
3. ChromaDB will be built at ./chroma_db/

PDF Sources:
- India Code: https://indiacode.nic.in
- IP India: https://ipindia.gov.in
- WIPO Treaties: https://wipo.int/treaties
- Ayush: https://ayush.gov.in
- NBA: https://nbaindia.org
"""

import os
import glob
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# ── Config ───────────────────────────────────────────────────
PDF_DIR = "./data/raw_pdfs"
CHROMA_DB_PATH = "./chroma_db"

# Jurisdictions — put PDFs in correct subfolder
INDIA_PDF_DIR = os.path.join(PDF_DIR, "india")
INTERNATIONAL_PDF_DIR = os.path.join(PDF_DIR, "international")

# ── Embedding model ──────────────────────────────────────────
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# ── Text splitter ────────────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " "]
)


def load_and_split_pdfs(pdf_dir: str) -> list:
    """Load all PDFs from a directory and split into chunks."""
    all_chunks = []
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))

    if not pdf_files:
        print(f"  No PDFs found in {pdf_dir}")
        return []

    for pdf_path in pdf_files:
        print(f"  Loading: {os.path.basename(pdf_path)}")
        loader = PyMuPDFLoader(pdf_path)
        pages = loader.load()
        chunks = splitter.split_documents(pages)

        # Tag each chunk with source metadata
        for chunk in chunks:
            chunk.metadata["source_file"] = os.path.basename(pdf_path)

        all_chunks.extend(chunks)
        print(f"    → {len(chunks)} chunks")

    return all_chunks


def build_vectorstore(chunks: list, collection_name: str):
    """Store chunks in ChromaDB under given collection name."""
    if not chunks:
        print(f"  Skipping {collection_name} — no chunks")
        return

    print(f"\nBuilding ChromaDB collection: {collection_name}")
    print(f"Total chunks: {len(chunks)}")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=CHROMA_DB_PATH
    )
    print(f"Done — saved to {CHROMA_DB_PATH}")


if __name__ == "__main__":
    print("=" * 50)
    print("IP-SAKTI Corpus Builder")
    print("=" * 50)

    # Build India Laws vectorstore
    print("\n[1/2] Processing Indian Laws PDFs...")
    india_chunks = load_and_split_pdfs(INDIA_PDF_DIR)
    build_vectorstore(india_chunks, "india_laws")

    # Build International Laws vectorstore
    print("\n[2/2] Processing International Laws PDFs...")
    intl_chunks = load_and_split_pdfs(INTERNATIONAL_PDF_DIR)
    build_vectorstore(intl_chunks, "international_laws")

    print("\nCorpus build complete!")
    print(f"India chunks: {len(india_chunks)}")
    print(f"International chunks: {len(intl_chunks)}")
