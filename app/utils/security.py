import os
import bcrypt
import hashlib
import base64
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError

# --- CONFIG (Logic Preserved) ---
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_ME_IN_PROD")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# --- HASHING (Fixed for 72-byte limit & Passlib bugs) ---
def hash_password(password: str) -> str:
    """Pre-hash with SHA256 to bypass 72-byte limit, then use direct bcrypt."""
    inner_hash = hashlib.sha256(password.encode("utf-8")).digest()
    b64_pw = base64.b64encode(inner_hash)

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(b64_pw, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify using SHA256 pre-hash and direct bcrypt check."""
    try:
        inner_hash = hashlib.sha256(plain_password.encode("utf-8")).digest()
        b64_pw = base64.b64encode(inner_hash)
        return bcrypt.checkpw(b64_pw, hashed_password.encode("utf-8"))
    except Exception:
        return False

# --- JWT HANDLING (Logic Preserved) ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """
    REQUIRED BY AUTH ROUTER: Decodes the JWT or returns empty dict.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return {}