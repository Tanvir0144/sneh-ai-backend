from fastapi import APIRouter, Response

router = APIRouter()

# This will handle GET requests (like from your browser)
@router.get("/health", tags=["Health"])
async def health_check_get():
    """
    Check if the API is running.
    """
    return {"status": "ok"}

# --- THIS IS THE NEW ADDITION ---
# This will specifically handle HEAD requests (like from UptimeRobot)
@router.head("/health", tags=["Health"])
async def health_check_head():
    """
    Respond to HEAD requests for health checks from monitoring services.
    """
    return Response(status_code=200)
# --- END OF ADDITION ---
