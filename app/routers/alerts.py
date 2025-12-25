from fastapi import APIRouter
from app.db import sensor_collection
from app.services.alerts import evaluate_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/latest/{device_id}")
def get_latest_alerts(device_id: str):
    data = sensor_collection.find_one(
        {"device_id": device_id},
        {"_id": 0},
        sort=[("timestamp", -1)]
    )

    if not data:
        return {
            "device_id": device_id,
            "alerts": [],
            "message": "No data found"
        }

    alerts = evaluate_alerts(data)

    return {
        "device_id": device_id,
        "alerts": alerts,
        "status": "critical" if alerts else "normal"
    }
