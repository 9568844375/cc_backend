# === FILE: utils/intent_classifier.py ===
def classify_intent(message):
    message = message.lower()
    if "resume" in message:
        return "resume_review"
    if "proposal" in message:
        return "proposal_help"
    if "event" in message:
        return "event_query"
    if "upload" in message:
        return "document_qa"
    return "general"