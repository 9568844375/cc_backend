# === FILE: cc_backend_file/main.py ===

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from dotenv import load_dotenv
from fastapi import FastAPI, Depends,Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Add Lexie to path
sys.path.append(os.path.join(os.path.dirname(__file__), "lexie"))

# Load env vars
load_dotenv()

# Import from Lexie config
from lexie.config import REDIS_URL, FRONTEND_URL, STATIC_DIR

# === Campus Connect routers ===
from routes.auth import router as auth_router
from routes.admin import router as admin_router
from routes.teacher import router as teacher_router
from routes.student import router as student_router
from routes.organization import router as org_router

# === Lexie AI routers ===
from lexie.routes.chat import router as lexie_chat_router
from lexie.routes.upload import router as upload_router
from lexie.routes.feedback import router as feedback_router
from lexie.routes.voice_chat import router as voice_router
from lexie.routes.auth import router as lexie_auth_router
from lexie.routes.admin import router as lexie_admin_router


app = FastAPI(title="Campus Connect + Lexie AI")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("❌ Validation Error:", exc.errors())
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Invalid input", "details": exc.errors()},
    )


# === Static files (for TTS audio, etc.) ===
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# === Redis for Rate Limiting / Memory ===
@app.on_event("startup")
async def startup():
    redis_client = redis.from_url(REDIS_URL)
    await FastAPILimiter.init(redis_client)

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # or [FRONTEND_URL] for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Campus Connect routes ===
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin_router, prefix="/api/admin", tags=["Campus Admin"])
app.include_router(teacher_router, prefix="/api/teacher", tags=["Campus Teacher"])
app.include_router(student_router, prefix="/api/student", tags=["Campus Student"])
app.include_router(org_router, prefix="/api/organization", tags=["Campus Organization"])


# === Lexie AI routes ===
app.include_router(lexie_auth_router, prefix="/oauth", tags=["OAuth2"])
app.include_router(lexie_chat_router, prefix="/lexie/chat", tags=["Lexie Chat"], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
app.include_router(upload_router, prefix="/lexie/upload", tags=["Lexie Upload"])
app.include_router(feedback_router, prefix="/lexie/feedback", tags=["Lexie Feedback"])
app.include_router(voice_router, prefix="/lexie/voice", tags=["Lexie Voice"])
app.include_router(lexie_admin_router, prefix="/lexie/admin", tags=["Lexie Admin"])
