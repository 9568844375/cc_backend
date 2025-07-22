# === test_groq.py ===
import asyncio
from utils.groq_client import query_groq

messages = [
    {"role": "system", "content": "You are Lexie, a helpful AI assistant."},
    {"role": "user", "content": "What's 2 + 2?"}
]

async def test_groq():
    result = await query_groq(messages)
    print("✅ Groq response:", result)

asyncio.run(test_groq())
