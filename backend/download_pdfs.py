"""
PDF Downloader — Run this once to download all required legal documents.

Usage:
    python download_pdfs.py
"""

import os
import requests
import time

# ── India PDFs ───────────────────────────────────────────────
INDIA_PDFS = {
    "patents_act_1970.pdf": (
        "https://naarm.org.in/VirtualLearning/vlc/IPR/Acts2004/patents/IPA_1970.pdf"
    ),
    "trademarks_act_1999.pdf": (
        "https://www.bombayhighcourt.gov.in/bhc/libweb/legislation/actc/1999.47.pdf"
    ),
    "gi_act_1999.pdf": (
        "https://www.dpiit.gov.in/static/uploads/2025/06/00de435f5dae279a801361e80ad41452.pdf"
    ),
    "biological_diversity_act.pdf": (
        "https://nbaindia.org/uploaded/docs/bio.diversity.act.pdf"
    ),
    "drugs_cosmetics_act.pdf": (
        "https://courtkutchehry-s3.s3.ap-south-1.amazonaws.com/bare_acts/trade-marks-act,-1999.pdf"
    ),
}

# ── International PDFs ───────────────────────────────────────
INTERNATIONAL_PDFS = {
    "trips_agreement.pdf": (
        "https://www.wto.org/english/docs_e/legal_e/27-trips.pdf"
    ),
    "nagoya_protocol.pdf": (
        "https://www.cbd.int/abs/doc/protocol/nagoya-protocol-en.pdf"
    ),
    "cbd_convention.pdf": (
        "https://www.cbd.int/doc/legal/cbd-en.pdf"
    ),
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    )
}


def download_pdf(url: str, save_path: str):
    """Download one PDF with progress indicator."""
    filename = os.path.basename(save_path)
    print(f"  Downloading: {filename}")
    print(f"  URL: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)

        size_kb = os.path.getsize(save_path) / 1024
        print(f"  Done — {size_kb:.1f} KB saved\n")
        return True

    except Exception as e:
        print(f"  FAILED: {e}")
        print(f"  Manually download from: {url}\n")
        return False


def main():
    print("=" * 60)
    print("IP-SAKTI PDF Downloader")
    print("=" * 60)

    # Create directories
    india_dir = "./data/raw_pdfs/india"
    intl_dir  = "./data/raw_pdfs/international"
    os.makedirs(india_dir, exist_ok=True)
    os.makedirs(intl_dir,  exist_ok=True)

    # Download India PDFs
    print("\n[1/2] Indian Law PDFs")
    print("-" * 40)
    india_ok = 0
    for filename, url in INDIA_PDFS.items():
        path = os.path.join(india_dir, filename)
        if os.path.exists(path):
            print(f"  SKIP (already exists): {filename}\n")
            india_ok += 1
            continue
        if download_pdf(url, path):
            india_ok += 1
        time.sleep(1)   # be polite to servers

    # Download International PDFs
    print("\n[2/2] International Treaty PDFs")
    print("-" * 40)
    intl_ok = 0
    for filename, url in INTERNATIONAL_PDFS.items():
        path = os.path.join(intl_dir, filename)
        if os.path.exists(path):
            print(f"  SKIP (already exists): {filename}\n")
            intl_ok += 1
            continue
        if download_pdf(url, path):
            intl_ok += 1
        time.sleep(1)

    # Summary
    print("=" * 60)
    print(f"India PDFs:         {india_ok}/{len(INDIA_PDFS)}")
    print(f"International PDFs: {intl_ok}/{len(INTERNATIONAL_PDFS)}")

    if india_ok + intl_ok == len(INDIA_PDFS) + len(INTERNATIONAL_PDFS):
        print("\nAll PDFs ready!")
        print("Next step: python -m app.services.corpus_builder")
    else:
        print("\nSome PDFs failed — download manually from links above")
        print("Place them in the correct folder and run corpus_builder")
    print("=" * 60)


if __name__ == "__main__":
    main()
