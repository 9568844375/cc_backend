# === FILE: lexie/utils/voice_chat.py ===
import os
import whisper
from gtts import gTTS
from uuid import uuid4
from .lang_detect import detect_language  # ⬅️ Fixed import
import redis.asyncio as redis
import hashlib
import time



print("✅ voice_chat.py is being loaded")

# Whisper STT
model = whisper.load_model("base")

# Redis cache
cache = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Static dir setup
STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)

# Auto-delete old mp3s (>1 hr)
EXPIRY_SECONDS = 3600
def cleanup_old_audio():
    now = time.time()
    for f in os.listdir(STATIC_DIR):
        path = os.path.join(STATIC_DIR, f)
        if f.endswith(".mp3") and now - os.path.getmtime(path) > EXPIRY_SECONDS:
            os.remove(path)
            print(f"🗑️ Deleted old audio file: {f}")

# Speech to Text
def transcribe_audio(audio_bytes):
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    result = model.transcribe("temp.wav")
    return result["text"]

# Text to Speech
async def speak_text(text):
    cleanup_old_audio()

    # Cache check
    cache_key = hashlib.sha256(text.encode()).hexdigest()
    cached = await cache.get(cache_key)
    if cached:
        print("🔁 Using cached audio")
        return cached

    lang = detect_language(text)
    tts = gTTS(text=text, lang=lang)
    filename = f"tts_{uuid4().hex}.mp3"
    path = os.path.join(STATIC_DIR, filename)
    tts.save(path)

    await cache.set(cache_key, filename, ex=EXPIRY_SECONDS)
    print(f"✅ TTS generated and cached: {filename}")
    return filename

print("transcribe_audio exists:", callable(transcribe_audio))
print("speak_text exists:", callable(speak_text))
