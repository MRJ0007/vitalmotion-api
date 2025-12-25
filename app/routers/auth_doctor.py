from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db import doctors_collection
from app.core.security import verify_password
from app.core.jwt import create_access_token

router = APIRouter(prefix="/auth/doctor", tags=["Doctor Auth"])

doctors = doctors_collection


# ---------------- LOGIN SCHEMA ----------------

class DoctorLoginRequest(BaseModel):
    email: str
    password: str


# ---------------- LOGIN ENDPOINT ----------------

@router.post("/login")
def doctor_login(payload: DoctorLoginRequest):

    # =====================================================
    # 🔹 DEMO-ONLY DOCTOR (NO DB, NO COSMOS RU ISSUES)
    # =====================================================
    if payload.email == "doctor3@hospital.com" and payload.password == "Doctor@123":
        token = create_access_token({
            "sub": payload.email,
            "role": "doctor"
        })
        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "doctor"
        }

    # =====================================================
    # 🔹 FUTURE: DB-BASED DOCTORS (ADMIN CREATED)
    # =====================================================
    doctor = doctors.find_one({"email": payload.email})

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not doctor.get("is_active", False):
        raise HTTPException(status_code=403, detail="Doctor disabled")

    if not verify_password(payload.password, doctor["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": doctor["email"],
        "role": "doctor"
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "doctor"
    }
