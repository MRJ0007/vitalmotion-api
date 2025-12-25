from fastapi import APIRouter
from datetime import datetime
from pymongo.errors import PyMongoError

from app.schemas.sensor import SensorData
from app.db import sensor_collection
from app.core.live_store import LIVE_SENSORS

# 🔵 OPTIONAL anomaly buffer (safe import)
try:
    from app.core.anomaly_buffer import push as anomaly_push
except Exception:
    anomaly_push = None  # failsafe

router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"]
)


@router.post("/sensor")
def ingest_sensor(data: SensorData):
    record = data.model_dump()
    record["timestamp"] = datetime.utcnow().isoformat()

    # 🔴 LIVE SENSOR UPDATE (REAL-TIME DASHBOARD)
    LIVE_SENSORS[data.device_id] = {
        "device_id": data.device_id,
        "heart_rate": data.heart_rate,
        "spo2": data.spo2,
        "temperature": data.temperature,
        "timestamp": record["timestamp"]
    }

    # 🟢 ANOMALY BUFFER (NON-BLOCKING, OPTIONAL)
    if anomaly_push:
        try:
            anomaly_push(data.device_id, LIVE_SENSORS[data.device_id])
        except Exception:
            pass  # NEVER stop ingestion

    # 🟡 TRY COSMOS WRITE (NON-BLOCKING)
    try:
        sensor_collection.insert_one(record)
        db_status = "stored"
    except PyMongoError:
        db_status = "skipped"

    return {
        "status": "ok",
        "db": db_status,
        "device_id": data.device_id,
        "timestamp": record["timestamp"]
    }
