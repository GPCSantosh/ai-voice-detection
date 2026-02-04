import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from audio_utils import load_audio_from_base64
from model import detect_ai_voice
from honeypot import process_honeypot_message
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(title="AI Voice Detection API")

API_KEY = os.getenv("API_KEY")

SUPPORTED_LANGUAGES = [
    "Tamil", "English", "Hindi", "Malayalam", "Telugu"
]

class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

@app.post("/api/voice-detection")
def voice_detection(
    data: VoiceRequest,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if data.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    if data.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Only MP3 supported")

    try:
        y, sr = load_audio_from_base64(data.audioBase64)
        result = detect_ai_voice(y, sr)
    except Exception:
        raise HTTPException(status_code=400, detail="Audio processing error")

    return {
        "status": "success",
        "language": data.language,
        "classification": result["classification"],
        "confidenceScore": result["confidence"],
        "explanation": result["explanation"]
    }
from typing import Optional

class HoneypotRequest(BaseModel):
    message: Optional[str] = None
@app.post("/api/honeypot")
def honeypot_endpoint(
    data: Optional[HoneypotRequest] = None,
    x_api_key: str = Header(None)
):
    if not x_api_key or x_api_key.strip() != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # If tester sends no body
    if not data or not data.message:
        return {
            "status": "success",
            "response": "Can you explain more?"
        }

    # Honeypot logic
    _, reply = process_honeypot_message(data.message)

    return {
        "status": "success",
        "response": reply
    }
