from fastapi import APIRouter, Depends, UploadFile, File

from app.db import models
from app.schemas.voice import TTSRequest, TTSResponse, STTResponse
from app.api.v1 import deps
from app.services import voice_service

router = APIRouter()

@router.post("/stt", response_model=STTResponse)
async def speech_to_text(
    *,
    current_user: models.User = Depends(deps.get_current_user),
    file: UploadFile = File(...)
):
    """
    Convert spoken audio from a file into text.
    """
    # Call the REAL async function
    transcribed_text = await voice_service.convert_speech_to_text(file)
    return STTResponse(transcribed_text=transcribed_text)

@router.post("/tts", response_model=TTSResponse)
def text_to_speech(
    *,
    current_user: models.User = Depends(deps.get_current_user),
    tts_request: TTSRequest
):
    """
    Convert text into a natural-sounding audio file URL.
    """
    # Call the REAL function
    audio_url = voice_service.convert_text_to_speech(text=tts_request.text)
    return TTSResponse(audio_url=audio_url)