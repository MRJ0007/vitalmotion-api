from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# -----------------------------
# SIGNUP
# -----------------------------
class SignupRequest(BaseModel):
    email: EmailStr
    phone: str = Field(..., example="+919876543210")
    role: str = Field(..., example="user") # 'user' or 'doctor'

class SignupResponse(BaseModel):
    message: str

# -----------------------------
# OTP
# -----------------------------
class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)

class VerifyOtpResponse(BaseModel):
    message: str

# -----------------------------
# PASSWORD
# -----------------------------
class CreatePasswordRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class CreatePasswordResponse(BaseModel):
    message: str

# -----------------------------
# LOGIN
# -----------------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

# -----------------------------
# ME (Used for Auth Guards)
# -----------------------------
class UserMeResponse(BaseModel):
    email: EmailStr
    role: str
    model_config = {"from_attributes": True} # Allows DB object to Pydantic conversion