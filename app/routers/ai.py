# app/routers/ai.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.services.ai_service import analyze_vitals
from app.security import get_current_user

router = APIRouter(prefix="/ai", tags=["AI"])


# ============================
# REQUEST MODEL (DEMO-SAFE)
# ============================
class AIAnalyzeRequest(BaseModel):
    device_id: Optional[str] = Field(default="vm-001")
    heart_rate: int = Field(..., ge=0, le=250)
    spo2: int = Field(..., ge=0, le=100)
    temperature: float = Field(..., ge=30.0, le=45.0)


# ============================
# RESPONSE MODEL
# ============================
class AIAnalyzeResponse(BaseModel):
    status: str
    severity: int
    risks: list[str]
    ai_insight: str
    generated_at: datetime


# ============================
# OPTIONAL AUTH (NO 401)
# ============================
def get_user_optional():
    try:
        return get_current_user()
    except Exception:
        return None


# ============================
# ROUTE
# ============================
@router.post("/analyze", response_model=AIAnalyzeResponse)
def analyze(
        data: AIAnalyzeRequest,
        user: Optional[dict] = Depends(get_user_optional),
):
    vitals = {
        "heart_rate": data.heart_rate,
        "spo2": data.spo2,
        "temperature": data.temperature,
    }

    role = user.get("role") if user else "user"
    return analyze_vitals(vitals, role)
