"""
Security utilities for authentication and authorization
Includes password hashing and JWT token management
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from jwt.exceptions import PyJWTError
from passlib.context import CryptContext
from .config import settings

# Password hashing context (bcrypt with 12 rounds)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash

    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored password hash

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token

    Args:
        data: Data to encode in the token (typically {"sub": username})
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT refresh token with longer expiration

    Args:
        data: Data to encode in the token

    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except PyJWTError:
        return None


def hash_id_number(id_number: str) -> str:
    """
    Hash an ID number using SHA-256 for privacy in QR codes

    Args:
        id_number: Government ID number (Aadhaar, PAN, etc.)

    Returns:
        SHA-256 hash of the ID number
    """
    import hashlib
    return hashlib.sha256(id_number.encode()).hexdigest()


def create_hmac_signature(data: str, secret: Optional[str] = None) -> str:
    """
    Create HMAC-SHA256 signature for QR code validation

    Args:
        data: Data to sign (JSON string of QR code content)
        secret: Optional secret key (uses JWT secret if not provided)

    Returns:
        HMAC-SHA256 signature hex string
    """
    import hmac
    import hashlib

    key = secret or settings.JWT_SECRET_KEY
    signature = hmac.new(
        key.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature


def verify_hmac_signature(data: str, signature: str, secret: Optional[str] = None) -> bool:
    """
    Verify HMAC-SHA256 signature

    Args:
        data: Original data that was signed
        signature: Signature to verify
        secret: Optional secret key

    Returns:
        True if signature is valid, False otherwise
    """
    expected_signature = create_hmac_signature(data, secret)
    return hmac.compare_digest(signature, expected_signature)
