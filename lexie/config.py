# === FILE: lexie/config.py ===
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from root .env file
load_dotenv()

# Base directory = root of the Lexie folder
BASE_DIR = Path(__file__).resolve().parent

# Load the Lexie prompt from prompts/ folder
LEXIE_PROMPT = ""
try:
    with open(BASE_DIR / "prompts" / "lexie_prompt.txt", "r", encoding="utf-8") as f:
        LEXIE_PROMPT = f.read()
except FileNotFoundError:
    print("⚠️  Warning: lexie_prompt.txt not found.")

# Secret key (used in JWT or session signing)
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")  # ✅ Add this
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")  # ✅ Add this
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Groq API Key (for LLM access)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# MongoDB settings (optional – used by Lexie)
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "campus_connect")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "users")

# Redis for rate limiting/memory
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

LOG_DIR = os.getenv("LOG_DIR", "logs")
REPORT_DIR = os.getenv("REPORT_DIR", "reports")
STATIC_DIR = os.getenv("STATIC_DIR", "static")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# ✅ ADD THIS LINE TO FIX YOUR ERROR
VECTOR_INDEX_PATH = os.getenv("VECTOR_INDEX_PATH", "data/faiss_index")
