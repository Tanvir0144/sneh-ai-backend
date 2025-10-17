from pydantic import BaseModel

# For Text-to-Speech request
class TTSRequest(BaseModel):
    text: str

# For Text-to-Speech response
class TTSResponse(BaseModel):
    audio_url: str

# For Speech-to-Text response
class STTResponse(BaseModel):
    transcribed_text: str