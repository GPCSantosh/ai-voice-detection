# model.py
import numpy as np
import librosa

def detect_ai_voice(y, sr):
    pitch = librosa.yin(y, fmin=50, fmax=300)
    pitch = pitch[~np.isnan(pitch)]

    pitch_std = np.std(pitch)
    pitch_mean = np.mean(pitch)

    if pitch_std < 8:
        return {
            "classification": "AI_GENERATED",
            "confidence": round(min(1.0, 0.75 + (8 - pitch_std) * 0.03), 2),
            "explanation": "Unnatural pitch stability detected"
        }
    else:
        return {
            "classification": "HUMAN",
            "confidence": round(min(1.0, 0.70 + (pitch_std - 8) * 0.02), 2),
            "explanation": "Natural pitch variation detected"
        }
