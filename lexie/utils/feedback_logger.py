# === FILE: utils/feedback_logger.py ===
from datetime import datetime
from database import feedback_collection  # ✅ Shared DB connection

def log_feedback(user_id, message_id, feedback):
     # ✅ Validate feedback value
    if feedback not in ["like", "dislike"]:
        raise ValueError("Feedback must be either 'like' or 'dislike'")
    entry = {
        "user_id": user_id,
        "message_id": message_id,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat()
    }
    feedback_collection.insert_one(entry)
