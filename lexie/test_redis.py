# === test_redis.py ===
import asyncio
import redis.asyncio as redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def test_redis():
    test_key = "test_user"
    test_value = [{"user": "Hi", "bot": "Hello"}]
    
    await r.set(test_key, json.dumps(test_value))
    result = await r.get(test_key)
    print("✅ Redis result:", result)

asyncio.run(test_redis())
