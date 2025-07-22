import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
print("GROQ_API_KEY:", GROQ_API_KEY)
async def query_groq(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",  # ✅ updated to valid model
        "messages": messages,
        "temperature": 0.7,
        "stream": False
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(GROQ_URL, json=payload, headers=headers)

    # Debugging: Show raw response for testing
    print("📦 Groq Raw Response:", resp.status_code, resp.text)

    if resp.status_code != 200:
        raise Exception(f"Groq API error: {resp.text}")

    return resp.json()["choices"][0]["message"]["content"]
