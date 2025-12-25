from fastapi import APIRouter
from app.db import sensor_collection
from app.core.live_store import LIVE_SENSORS

router = APIRouter(prefix="/sensor", tags=["Sensor"])


# 🔴 LIVE SENSOR (REAL-TIME, NO DB)
@router.get("/live/{device_id}")
def get_live_sensor(device_id: str):
    return LIVE_SENSORS.get(
        device_id,
        {
            "device_id": device_id,
            "heart_rate": 0,
            "spo2": 0,
            "temperature": 0,
            "timestamp": None
        }
    )


# 🟣 LATEST STORED SENSOR (COSMOS)
@router.get("/latest/{device_id}")
def get_latest_sensor(device_id: str):
    data = sensor_collection.find_one(
        {"device_id": device_id},
        {"_id": 0},
        sort=[("timestamp", -1)]
    )

    if not data:
        return {"message": "No data found"}

    return data


# 🟣 SENSOR HISTORY (COSMOS)
@router.get("/history/{device_id}")
def get_sensor_history(device_id: str):
    cursor = (
        sensor_collection.find(
            {"device_id": device_id},
            {"_id": 0}
        )
        .sort("timestamp", -1)
        .limit(20)
    )

    return list(cursor)
