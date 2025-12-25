import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. LOAD ENV FIRST
load_dotenv()
print(f"🔥 GEMINI_API_KEY = {'LOADED' if os.getenv('GEMINI_API_KEY') else 'NONE'}")

app = FastAPI(title="VitalMotion API")

# 2. UNIVERSAL CORS CONFIG (Optimized for Vercel + Render)
# This removes the "Blocked by CORS" error by allowing all origins.
# Since you use JWT tokens, allow_credentials=False is the correct setting.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allows all domains (fixes Vercel connection)
    allow_credentials=False,   # Must be False when using "*"
    allow_methods=["*"],      # Allows all actions (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],      # Allows Authorization and Content-Type headers
)

# 3. ROUTER REGISTRATION
from app.routers import (
    health, ai, sensor, alerts, ingest,
    auth_doctor, admin, auth, chat, vision
)

# Include routers
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

@app.get("/")
def home():
    return {
        "status": "VitalMotion API is Online",
        "message": "CORS set to Universal Mode"
    }