import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. LOAD ENV FIRST
load_dotenv()
print(f"🔥 GEMINI_API_KEY = {'LOADED' if os.getenv('GEMINI_API_KEY') else 'NONE'}")

app = FastAPI(title="VitalMotion API")

# 2. CORS (SMART CONFIG)
# This allows both your local dev server and your real website domain.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://vitalmotion.xyz",
    "https://www.vitalmotion.xyz",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. ROUTER REGISTRATION (FIXED PREFIXES)
from app.routers import (
    health, ai, sensor, alerts, ingest,
    auth_doctor, admin, auth, chat, vision
)

# NOTE: If your routers (auth.py, etc.) already have prefix="/auth",
# do NOT add prefix="/auth" here or you get /auth/auth/login.
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
    return {"status": "VitalMotion API is Online"}