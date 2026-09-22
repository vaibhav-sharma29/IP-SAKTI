from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    """
    Simple health check — frontend calls this to verify backend is alive.
    Frontend shows a green/red dot based on this response.
    """
    return {"status": "ok", "service": "IP-SAKTI Backend"}
