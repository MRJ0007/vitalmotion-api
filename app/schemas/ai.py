from pydantic import BaseModel
from datetime import datetime

class VitalsInput(BaseModel):
    heart_rate: int | None = None
    spo2: int | None = None
    temperature: float | None = None


class AIResponse(BaseModel):
    status: str
    severity: int
    risks: list[str]
    ai_insight: str
    generated_at: datetime
