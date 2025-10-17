import os
import uuid
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

# Import the new, specific clients that we installed
from google.cloud import texttospeech
from google.cloud import speech

# Set the environment variable for authentication directly in the code
if settings.GOOGLE_APPLICATION_CREDENTIALS_PATH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS_PATH

def convert_text_to_speech(text: str) -> str:
    """
    Converts text to speech using the dedicated Google Cloud TTS API.
    """
    try:
        # Instantiate a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        audio_bytes = response.audio_content

        # Save the audio file
        audio_dir = os.path.join("static", "audio")
        os.makedirs(audio_dir, exist_ok=True)
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(audio_dir, audio_filename)

        with open(audio_path, "wb") as f:
            f.write(audio_bytes)

        return f"{settings.BASE_URL}/static/audio/{audio_filename}"

    except Exception as e:
        print(f"Text-to-Speech API call failed: {e}")
        raise e

async def convert_speech_to_text(file: UploadFile) -> str:
    """
    Converts speech to text using the dedicated Google Cloud Speech-to-Text API.
    """
    try:
        client = speech.SpeechClient()
        audio_content = await file.read()
        audio = speech.RecognitionAudio(content=audio_content)
        
        content_type = file.content_type
        encoding_map = {
            "audio/mpeg": speech.RecognitionConfig.AudioEncoding.MP3,
            "audio/wav": speech.RecognitionConfig.AudioEncoding.LINEAR16,
            "audio/flac": speech.RecognitionConfig.AudioEncoding.FLAC,
            "audio/ogg": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            "audio/amr": speech.RecognitionConfig.AudioEncoding.AMR,
        }

        encoding = encoding_map.get(content_type)
        
        if not encoding:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported audio format: {content_type}. Please use MP3, WAV, FLAC, or OGG."
            )

        # --- FIX STARTS HERE ---
        # Configuration without the 'model' parameter.
        # Let Google choose the best default model.
        config = speech.RecognitionConfig(
            encoding=encoding,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
        # --- FIX ENDS HERE ---

        response = client.recognize(config=config, audio=audio)

        if response.results:
            return response.results[0].alternatives[0].transcript
        else:
            return "No speech was recognized."
            
    except Exception as e:
        print(f"Speech-to-Text API call failed: {e}")
        raise e