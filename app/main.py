import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from dotenv import load_dotenv

# -------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# -------------------------------------------------
load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
print(f"🔥 GEMINI_API_KEY = {'LOADED' if gemini_key else 'NONE'}")

# -------------------------------------------------
# 2. CREATE FASTAPI APP
# -------------------------------------------------
app = FastAPI(title="VitalMotion API")

# -------------------------------------------------
# 3. CORS CONFIGURATION (LOCAL + PRODUCTION)
# MUST BE BEFORE ROUTERS
# -------------------------------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://vitalmotion-ui.vercel.app",
    "https://vitalmotion-ui.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# 4. GLOBAL OPTIONS HANDLER (CRITICAL FIX)
# Prevents auth dependencies from blocking preflight
# -------------------------------------------------
@app.options("/{full_path:path}")
async def preflight_handler(request: Request, full_path: str):
    return Response(status_code=200)

# -------------------------------------------------
# 5. ROUTER IMPORTS (AFTER CORS + OPTIONS)
# -------------------------------------------------
from app.routers import (
    health,
    ai,
    sensor,
    alerts,
    ingest,
    auth_doctor,
    admin,
    auth,
    chat,
    vision,
)

# -------------------------------------------------
# 6. ROUTER REGISTRATION
# -------------------------------------------------
app.include_router(auth.router)
app.include_router(auth_doctor.router)
app.include_router(ai.router)
app.include_router(health.router)
app.include_router(sensor.router)
app.include_router(alerts.router)
app.include_router(ingest.router)
app.include_router(chat.router)
app.include_router(admin.router)
app.include_router(vision.router)

# -------------------------------------------------
# 7. ROOT / HEALTH CHECK
# -------------------------------------------------
@app.get("/")
def home():
    return {
        "status": "VitalMotion API is Online",
        "cors": "Explicit whitelist + global OPTIONS handler",
        "gemini_status": "Active" if gemini_key else "Inactive",
    }
