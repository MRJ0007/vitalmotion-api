from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt  # PyJWT logic preserved here
import os
import hashlib
import base64
from datetime import datetime, timedelta, timezone

# -------------------------------------------------
# CONFIG (Logic Preserved)
# -------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = os.getenv("JWT_SECRET", "your-super-secret-key-123")
ALGORITHM = "HS256"

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# -------------------------------------------------
# HASHING (Logic: PBKDF2 + 72-byte fix)
# -------------------------------------------------
def hash_password(password: str) -> str:
    pw_hash = base64.b64encode(hashlib.sha256(password.encode("utf-8")).digest()).decode("utf-8")
    return pwd_context.hash(pw_hash)

def verify_password(plain: str, hashed: str) -> bool:
    pw_hash = base64.b64encode(hashlib.sha256(plain.encode("utf-8")).digest()).decode("utf-8")
    return pwd_context.verify(pw_hash, hashed)

# -------------------------------------------------
# JWT & ROLE LOGIC (Logic Preserved)
# -------------------------------------------------
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=60))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(role: str):
    def checker(user=Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail=f"Access denied. Requires {role} role.")
        return user
    return checker