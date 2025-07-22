# === FILE: backend/utils/redis_memory.py ===
import redis.asyncio as redis
import json

print("✅ redis_memory.py loaded")

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def get_conversation_history(user_id):
    history = await r.get(user_id)
    return json.loads(history) if history else []

async def store_conversation(user_id, user_msg, bot_msg):
    history = await get_conversation_history(user_id)
    history.append({"user": user_msg, "bot": bot_msg})
    await r.set(user_id, json.dumps(history))
