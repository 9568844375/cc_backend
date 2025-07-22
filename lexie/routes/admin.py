# === FILE: routes/admin.py ===
from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/analytics")
async def get_analytics():
    data = []
    with open("logs/feedback.jsonl", "r") as f:
        for line in f:
            data.append(json.loads(line))
    return {"total_feedback": len(data), "entries": data[-10:]}

if __name__ == "__main__":
    print("✅ admin.py loaded")

