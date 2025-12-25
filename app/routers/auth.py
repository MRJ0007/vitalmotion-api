from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import os

from twilio.rest import Client

from app.schemas.auth import (
    SignupRequest,
    SignupResponse,
    VerifyOtpRequest,
    VerifyOtpResponse,
    CreatePasswordRequest,
    CreatePasswordResponse,
    LoginRequest,
    LoginResponse,
    UserMeResponse,
)

from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

from app.db import db

router = APIRouter(prefix="/auth", tags=["Auth"])

# -------------------------------------------------
# TWILIO (SANDBOX SAFE)
# -------------------------------------------------
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_PHONE")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def now_utc():
    return datetime.utcnow()

def otp_expiry():
    return now_utc() + timedelta(minutes=10)

def users_col():
    return db["users"]

# -------------------------------------------------
# SIGNUP
# -------------------------------------------------
@router.post("/signup", response_model=SignupResponse)
async def signup(data: SignupRequest):

    if data.role == "admin":
        raise HTTPException(status_code=403, detail="Admin signup not allowed")

    users = users_col()

    if users.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    otp = "123456"

    users.insert_one({
        "email": data.email,
        "phone": data.phone,
        "role": data.role,
        "password": None,
        "otp_verified": False,
        "otp_expires_at": otp_expiry(),
        "created_at": now_utc(),
    })

    try:
        twilio_client.messages.create(
            body=f"Your VitalMotion OTP is {otp}",
            from_=TWILIO_FROM,
            to=data.phone,
        )
    except Exception:
        pass

    return {"message": "OTP sent (sandbox: 123456)"}

# -------------------------------------------------
# VERIFY OTP
# -------------------------------------------------
@router.post("/verify-otp", response_model=VerifyOtpResponse)
async def verify_otp(data: VerifyOtpRequest):

    if data.otp != "123456":
        raise HTTPException(status_code=400, detail="Invalid OTP")

    users = users_col()
    user = users.find_one({"email": data.email, "otp_verified": False})

    if not user:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if user["otp_expires_at"] < now_utc():
        raise HTTPException(status_code=400, detail="OTP expired")

    users.update_one(
        {"_id": user["_id"]},
        {"$set": {"otp_verified": True}}
    )

    return {"message": "OTP verified"}

# -------------------------------------------------
# CREATE PASSWORD
# -------------------------------------------------
@router.post("/create-password", response_model=CreatePasswordResponse)
async def create_password(data: CreatePasswordRequest):

    users = users_col()
    user = users.find_one({"email": data.email, "otp_verified": True})

    if not user:
        raise HTTPException(status_code=400, detail="OTP verification required")

    users.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "password": hash_password(data.password),
            "otp_expires_at": None,
        }}
    )

    return {"message": "Password created"}

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):

    users = users_col()
    user = users.find_one({"email": data.email})

    if not user or not user.get("password"):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["email"],
        "role": user["role"],
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"],
    }

# -------------------------------------------------
# ME
# -------------------------------------------------
@router.get("/me", response_model=UserMeResponse)
async def me(token: str):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "email": payload["sub"],
        "role": payload["role"],
    }
