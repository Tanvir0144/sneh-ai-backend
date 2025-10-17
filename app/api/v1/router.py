from fastapi import APIRouter
from app.api.v1.endpoints import (
    health, 
    auth, 
    users, 
    chat, 
    image, 
    voice, 
    document, 
    payment,
    admin  # Import the new admin endpoint
)

api_router = APIRouter(prefix="/v1")

# Include all the endpoint routers here
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(image.router, prefix="/image", tags=["Image"])
api_router.include_router(voice.router, prefix="/voice", tags=["Voice"])
api_router.include_router(document.router, prefix="/document", tags=["Document"])
api_router.include_router(payment.router, prefix="/payment", tags=["Payment"])

# --- THIS IS THE NEW ADDITION ---
# Add the admin router to our main API router
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
# --- END OF ADDITION ---