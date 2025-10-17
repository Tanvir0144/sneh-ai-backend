import google.generativeai as genai
from app.core.config import settings

# Configure the Gemini API with the key from settings
try:
    if settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    pass

def get_ai_response(message: str) -> str:
    """
    Gets a response from the Google Gemini 2.5 Flash model.
    """
    if not settings.GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is not configured."

    try:
        # --- THIS IS THE FINAL, CORRECT MODEL NAME ---
        model = genai.GenerativeModel('gemini-2.5-flash')
        # --- CHANGE COMPLETE ---
        
        response = model.generate_content(message)
        
        return response.text
    except Exception as e:
        print(f"Gemini API call failed: {e}")
        return f"Sorry, I couldn't process your request due to an error: {e}"