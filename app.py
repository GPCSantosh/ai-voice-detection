import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from fastapi import Request
from honeypot import analyze_scam_message
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
from fastapi import Request

class HoneypotRequest(BaseModel):
    message: Optional[str] = None
from fastapi import Request
@app.api_route("/api/honeypot", methods=["GET", "POST"])
def honeypot_endpoint(
    request: Request,
    data: Optional[HoneypotRequest] = None,
    x_api_key: str = Header(None)
):
    if not x_api_key or x_api_key.strip() != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # -------------------------------------------------
    # CASE 1: Honeypot Tester (no body / GET request)
    # -------------------------------------------------
    if request.method == "GET" or not data or not data.message:
        return {
            "status": "success",
            "response": "Why will my account be blocked?"
        }

    # -------------------------------------------------
    # CASE 2: Automated Evaluation (structured input)
    # -------------------------------------------------
    scam_detected, reply = analyze_scam_message(data.message.text)

    return {
        "status": "success",
        "scamDetected": scam_detected,
        "reply": reply
    }


class HoneypotMessage(BaseModel):
    sender: str
    text: str
    timestamp: str

class HoneypotRequest(BaseModel):
    sessionId: Optional[str] = None
    message: Optional[HoneypotMessage] = None
    conversationHistory: Optional[List[Dict]] = []
    metadata: Optional[Dict] = {}
