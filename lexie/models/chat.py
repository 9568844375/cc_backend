# === FILE: models/chat.py ===

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class MessageInput(BaseModel):
    message: str
    user_id: Optional[str] = None
    user_role: Optional[str] = None
    user_profile: Optional[Dict[str, Any]] = None
    context: Optional[List[Dict[str, Any]]] = None
    uploaded_files: Optional[List[str]] = None
