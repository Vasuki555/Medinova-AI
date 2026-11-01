"""
Security Utilities
Password hashing and JWT token management.

Uses the `bcrypt` library directly (instead of passlib) for Python 3.14
compatibility — passlib's backend detection triggers a ValueError in
bcrypt ≥ 4.x when handling its internal 72-byte test password.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import bcrypt
from jose import JWTError, jwt
from app.config import settings


# ── Password hashing ─────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string (bcrypt, UTF-8 decoded)
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a bcrypt hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password stored in database

    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False


# ── JWT tokens ────────────────────────────────────────────────────────────────

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Payload dict (e.g. {"sub": user_id, "role": "patient"})
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: Dict) -> str:
    """
    Create a JWT refresh token with longer expiration.

    Args:
        data: Payload dict

    Returns:
        Encoded JWT refresh token string
    """
    import uuid
    
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Add JTI (JWT ID) for token revocation tracking
    jti = str(uuid.uuid4())
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
        "jti": jti
    })
    
    # Use separate refresh secret if configured, otherwise fall back to main secret
    refresh_secret = settings.JWT_REFRESH_SECRET_KEY or settings.JWT_SECRET_KEY
    return jwt.encode(to_encode, refresh_secret, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[Dict]:
    """
    Decode and verify a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload if valid, None otherwise
    """
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None


def verify_token(token: str) -> Optional[str]:
    """
    Verify JWT token and extract user ID.

    Args:
        token: JWT token string

    Returns:
        User ID (sub claim) if token is valid, None otherwise
    """
    payload = decode_token(token)
    if payload is None:
        return None
    return payload.get("sub")
