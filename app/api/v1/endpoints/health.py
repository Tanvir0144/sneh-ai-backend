from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Check if the API is running.
    """
    return {"status": "ok"}