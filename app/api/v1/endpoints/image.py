from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from app.schemas.image import ImageRequest, ImageResponse
from app.api.v1 import deps
from app.services import usage_service, image_service
from app.db.session import get_db

router = APIRouter()

@router.post("/generate", response_model=ImageResponse)
def generate_image(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user),
    image_request: ImageRequest,
):
    """
    Generate an image based on a text prompt using Google Imagen.
    Checks the user's daily usage limit before generating.
    """
    # Get user's usage and check limit
    usage = usage_service.get_or_create_usage(db, current_user)
    
    can_generate = usage_service.check_image_limit(current_user, usage)
    if not can_generate:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have reached your daily image generation limit."
        )

    try:
        # --- THIS IS THE MAIN CHANGE ---
        # Call the real Imagen generation service instead of the mock one
        image_url = image_service.generate_imagen_image(prompt=image_request.prompt)
        # --- CHANGE COMPLETE ---

        # Increment usage count only if image generation is successful
        usage.image_count += 1
        db.add(usage)
        db.commit()

        limit = usage_service.IMAGE_LIMITS.get(current_user.subscription_plan)
        usage_info = f"Usage: {usage.image_count}/{limit} for today."
        
        return ImageResponse(image_url=image_url, usage_info=usage_info)

    except Exception as e:
        # If anything goes wrong during image generation, return an error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate image: {str(e)}"
        )