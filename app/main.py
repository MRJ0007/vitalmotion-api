import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. LOAD ENV FIRST
load_dotenv()

# Verify Gemini API Key (Logic Preserved)
gemini_key = os.getenv("GEMINI_API_KEY")
print(f"🔥 GEMINI_API_KEY = {'LOADED' if gemini_key else 'NONE'}")

app = FastAPI(title="VitalMotion API")

# 2. CORS CONFIG (Fixed for Local + Production Handshake)
# Logic: We explicitly list localhost to allow Authorization headers.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://vitalmotion-ui.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Required for Bearer tokens and local development
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. ROUTER REGISTRATION (Logic Preserved)
from app.routers import (
    health, ai, sensor, alerts, ingest,
    auth_doctor, admin, auth, chat, vision
)

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
        "message": "CORS set to Explicit Origin Mode",
        "gemini_status": "Active" if gemini_key else "Inactive"
    }