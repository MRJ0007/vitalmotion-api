from fastapi import APIRouter
from app.schemas.ai import VitalsInput, AIResponse
from app.services.ai_service import analyze_vitals

router = APIRouter()

@router.post("/analyze", response_model=AIResponse)
def analyze(vitals: VitalsInput):
    return analyze_vitals(vitals.dict())
