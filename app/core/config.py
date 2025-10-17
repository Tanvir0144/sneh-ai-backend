from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Load .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Gemini API Key
    GEMINI_API_KEY: str | None = None
    
    # Google Cloud Platform (for Imagen & Voice)
    GCP_PROJECT_ID: str | None = None
    GCP_LOCATION: str | None = None
    
    # Path to the GCP Service Account JSON key file for authentication
    GOOGLE_APPLICATION_CREDENTIALS_PATH: str | None = None

    # PayPal Configuration
    PAYPAL_MODE: str | None = "sandbox"
    PAYPAL_CLIENT_ID: str | None = None
    PAYPAL_CLIENT_SECRET: str | None = None

    # --- THIS IS THE NEW ADDITION FOR DEPLOYMENT ---
    # Base URL for the server, used for creating absolute URLs
    BASE_URL: str = "http://localhost:8000"
    # --- END OF ADDITION ---


# Create a single instance of the settings
settings = Settings()