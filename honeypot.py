def process_honeypot_message(message: str):
    scam_keywords = [
        "blocked",
        "urgent",
        "verify",
        "account",
        "upi",
        "bank",
        "suspended"
    ]

    text = message.lower()
    scam_detected = any(word in text for word in scam_keywords)

    if scam_detected:
        reply = "Why will my account be blocked?"
    else:
        reply = "Can you explain more?"

    return scam_detected, reply
def analyze_scam_message(text: str):
    scam_keywords = [
        "blocked",
        "suspended",
        "urgent",
        "verify",
        "upi",
        "bank",
        "account",
        "freeze",
        "kyc"
    ]

    text_lower = text.lower()
    scam_detected = any(word in text_lower for word in scam_keywords)

    if scam_detected:
        reply = "Why will my account be blocked?"
    else:
        reply = "Can you explain more?"

    return scam_detected, reply
