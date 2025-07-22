# === FILE: routes/voice_chat.py ===

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from lexie.utils.voice_chat import transcribe_audio, speak_text

from utils.role_checker import get_current_user

router = APIRouter()

@router.post("/stt")
async def speech_to_text(
    audio: UploadFile = File(...),
    user=Depends(get_current_user)  # ✅ Require authenticated user
):
    try:
        audio_bytes = await audio.read()
        text = transcribe_audio(audio_bytes)
        print(f"🗣️ Transcribed for {user['role']}: {text}")
        return {"text": text}
    except Exception as e:
        print("❌ STT Error:", str(e))
        raise HTTPException(status_code=500, detail="Speech-to-text failed")

@router.post("/tts")
async def text_to_speech(
    text: str = "Hello from Lexie!",
    user=Depends(get_current_user)  # ✅ Require authenticated user
):
    try:
        filename = speak_text(text)
        print(f"🔊 Synthesized speech for {user['role']}")
        return {"audio_url": f"/static/{filename}"}
    except Exception as e:
        print("❌ TTS Error:", str(e))
        raise HTTPException(status_code=500, detail="Text-to-speech failed")
