import os
import uuid
import vertexai
from vertexai.vision_models import ImageGenerationModel
from app.core.config import settings

# Set the environment variable for authentication directly in the code
if settings.GOOGLE_APPLICATION_CREDENTIALS_PATH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS_PATH

# Initialize Vertex AI
try:
    if settings.GCP_PROJECT_ID and settings.GCP_LOCATION:
        vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_LOCATION)
except Exception as e:
    print(f"Error initializing Vertex AI: {e}")

def generate_imagen_image(prompt: str) -> str:
    """
    Generates an image using Google's stable Imagen model and saves it locally.
    Returns the absolute URL to the saved image.
    """
    if not (settings.GCP_PROJECT_ID and settings.GCP_LOCATION):
        raise ValueError("GCP_PROJECT_ID and GCP_LOCATION must be configured.")

    try:
        model = ImageGenerationModel.from_pretrained("imagegeneration@005")
        
        images = model.generate_images(
            prompt=prompt,
            number_of_images=1,
        )
        
        # --- THIS IS THE FIX ---
        # The 'GeneratedImage' object no longer has the '.image_bytes' attribute.
        # Instead, we use the '.save()' method provided by the library.
        
        image_filename = f"{uuid.uuid4()}.png"
        image_path = os.path.join("static", image_filename)

        # Get the first generated image object and save it directly to the path
        images[0].save(location=image_path)
        # --- FIX COMPLETE ---

        # Return the full, absolute URL to the image
        return f"{settings.BASE_URL}/static/{image_filename}"
        
    except Exception as e:
        print(f"Imagen API call failed: {e}")
        raise e