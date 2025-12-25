from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.hash import pbkdf2_sha256

from app.db import doctors
from app.security import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


# ---------------- SCHEMAS ---------------- #

class DoctorCreate(BaseModel):
    email: EmailStr
    password: str


class DoctorOut(BaseModel):
    email: EmailStr
    role: str
    active: bool


# ---------------- ROUTES ---------------- #

@router.post("/doctors")
def create_doctor(
        data: DoctorCreate,
        admin=Depends(require_role("admin"))
):
    if doctors.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Doctor already exists")

    doctors.insert_one({
        "email": data.email,
        "password": pbkdf2_sha256.hash(data.password),
        "role": "doctor",
        "active": True
    })

    return {"message": "Doctor created successfully"}


@router.get("/doctors", response_model=list[DoctorOut])
def list_doctors(
        admin=Depends(require_role("admin"))
):
    return list(
        doctors.find(
            {},
            {"_id": 0, "password": 0}
        )
    )


@router.patch("/doctors/{email}/status")
def update_doctor_status(
        email: str,
        active: bool,
        admin=Depends(require_role("admin"))
):
    res = doctors.update_one(
        {"email": email},
        {"$set": {"active": active}}
    )

    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {"message": "Doctor status updated"}
