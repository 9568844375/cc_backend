# === FILE: routes/feedback.py ===
from fastapi import APIRouter
from pydantic import BaseModel
from lexie.utils.feedback_logger import log_feedback


router = APIRouter()

class FeedbackModel(BaseModel):
    user_id: str
    message_id: str
    feedback: str  # 'like' or 'dislike'

@router.post("/")
async def feedback(data: FeedbackModel):
    log_feedback(data.user_id, data.message_id, data.feedback)
    return {"status": "logged"}
