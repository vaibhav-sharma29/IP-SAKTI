"""
Translation Service using Bhashini API (Govt of India — FREE)
Handles Hindi ↔ English translation for IP-SAKTI

Bhashini docs: https://bhashini.gov.in/ulca/search
Register for free API key at the above link.
"""

import httpx
from app.config import settings


BHASHINI_TRANSLATE_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"


async def translate_to_english(hindi_text: str) -> str:
    """
    Translates Hindi input to English before RAG processing.
    Falls back to original text if Bhashini is unavailable.
    """
    if not settings.bhashini_api_key:
        # Fallback: return as-is (Gemini handles Hindi somewhat)
        return hindi_text

    payload = {
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": "hi",
                        "targetLanguage": "en"
                    }
                }
            }
        ],
        "inputData": {
            "input": [{"source": hindi_text}]
        }
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                BHASHINI_TRANSLATE_URL,
                json=payload,
                headers={
                    "Authorization": settings.bhashini_api_key,
                    "Content-Type": "application/json"
                }
            )
            result = response.json()
            return result["pipelineResponse"][0]["output"][0]["target"]
    except Exception:
        # Graceful fallback — don't crash the app
        return hindi_text


async def translate_to_hindi(english_text: str) -> str:
    """
    Translates English RAG answer back to Hindi for display.
    Falls back to English if Bhashini is unavailable.
    """
    if not settings.bhashini_api_key:
        return english_text

    payload = {
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": "en",
                        "targetLanguage": "hi"
                    }
                }
            }
        ],
        "inputData": {
            "input": [{"source": english_text}]
        }
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                BHASHINI_TRANSLATE_URL,
                json=payload,
                headers={
                    "Authorization": settings.bhashini_api_key,
                    "Content-Type": "application/json"
                }
            )
            result = response.json()
            return result["pipelineResponse"][0]["output"][0]["target"]
    except Exception:
        return english_text
