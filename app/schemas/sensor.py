from pydantic import BaseModel, Field
from typing import Optional

class SensorData(BaseModel):
    device_id: str = Field(..., example="vm-001")

    heart_rate: Optional[int] = Field(
        None, example=75, ge=0, le=250
    )

    spo2: Optional[int] = Field(
        None, example=98, ge=0, le=100
    )

    temperature: Optional[float] = Field(
        None, example=36.8, ge=30.0, le=45.0
    )

    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "vm-001",
                "heart_rate": 88,
                "spo2": 96,
                "temperature": 37.2
            }
        }
