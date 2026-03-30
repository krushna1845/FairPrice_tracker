# ══════════════════════════════════════════════════════════════
#  core/security.py  —  Password Hashing & JWT Tokens
#
#  Handles two things:
#    1. Password security  → hash before saving, verify on login
#    2. JWT tokens         → create on login, decode on every request
#
#  JWT (JSON Web Token) is like a digital ID card:
#    - Created when user logs in
#    - Sent back to frontend
#    - Frontend includes it in every protected request header
#    - We decode it here to know WHO is making the request
# ══════════════════════════════════════════════════════════════

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings


# ── Password Hashing Setup ──────────────────────────────────────
# bcrypt is the industry standard for hashing passwords.
# It's slow by design — makes brute-force attacks very hard.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Converts a plain text password into a secure hash.
    
    Example:
        hash_password("mypassword123")
        → "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    
    We store the HASH in the database, never the real password.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if a plain password matches the stored hash.
    Returns True if correct, False if wrong.
    
    Example:
        verify_password("mypassword123", stored_hash)  → True
        verify_password("wrongpassword", stored_hash)  → False
    """
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT Token Functions ─────────────────────────────────────────

def create_access_token(data: dict) -> str:
    """
    Creates a JWT token containing user information.
    The token expires after ACCESS_TOKEN_EXPIRE_MINUTES (default 24 hours).
    
    Example:
        token = create_access_token({"sub": "user-uuid-here"})
        # Returns a long string like: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    payload = data.copy()

    # Set expiry time
    expire_time = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire_time})

    # Sign and encode the token using our SECRET_KEY
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def decode_access_token(token: str) -> dict | None:
    """
    Decodes a JWT token and returns its payload (the data inside it).
    Returns None if the token is invalid or expired.
    
    Example:
        payload = decode_access_token("eyJhbGci...")
        # Returns: {"sub": "user-uuid-here", "exp": 1234567890}
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        # Token is invalid, tampered, or expired
        return None
