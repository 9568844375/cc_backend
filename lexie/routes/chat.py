# === FILE: routes/chat.py ===

from fastapi import APIRouter, Depends, HTTPException
from lexie.models.chat import MessageInput
from utils.role_checker import get_current_user
from lexie.utils.redis_memory import get_conversation_history, store_conversation
from lexie.utils.vector_search import hybrid_search
from lexie.utils.tools_router import route_query_to_tool
from lexie.utils.groq_client import query_groq
from lexie.config import LEXIE_PROMPT

router = APIRouter()

@router.post("/")
async def chat_handler(data: MessageInput, user=Depends(get_current_user)):
    try:
        print("🔁 Received message:", data.message)
        user_id = str(user["_id"])
        role = user["role"]

        print("🔐 Authenticated user:", user["full_name"], "| Role:", role)

        # Retrieve chat memory
        history = await get_conversation_history(user_id)
        print("🧠 History:", history)

        # Hybrid vector + DB search
        relevant_docs = hybrid_search(data.message)
        print("📚 Retrieved Docs:", relevant_docs)

        # Tool routing (resume critic, analytics, etc.)
        tool_response = await route_query_to_tool(data.message, user_id, role)
        if tool_response:
            return {"reply": tool_response}

        # Prepare messages for LLM (Groq or OpenAI)
        messages = [{"role": "system", "content": LEXIE_PROMPT}]
        for pair in history:
            messages.append({"role": "user", "content": pair["user"]})
            messages.append({"role": "assistant", "content": pair["bot"]})
        messages.append({"role": "user", "content": data.message})

        print("📨 Sending to Groq:", messages)
        response = await query_groq(messages)
        print("🧠 Groq replied:", response)

        # Store updated conversation
        await store_conversation(user_id, data.message, response)

        return {
            "reply": response,
            "context": data.context  # Echoing context if needed on frontend
        }

    except Exception as e:
        print("❌ ERROR in /chat:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
