# audio_utils.py
import base64
import io
import librosa

def load_audio_from_base64(audio_base64: str):
    audio_bytes = base64.b64decode(audio_base64)
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(audio_buffer, sr=None)
    return y, sr
