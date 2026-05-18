from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
import secrets

from app.core.config import settings


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("lifelink.security")


# =========================================================
# PASSWORD HASHING
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# =========================================================
# TOKEN CREATION (COMMON CORE)
# =========================================================

def _create_token(
    data: Dict[str, Any],
    expires_delta: timedelta,
    token_type: str
) -> str:

    payload = data.copy()

    payload.update({
        "exp": datetime.utcnow() + expires_delta,
        "iat": datetime.utcnow(),
        "type": token_type,
        "jti": secrets.token_hex(16)
    })

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# =========================================================
# ACCESS TOKEN
# =========================================================

def create_access_token(data: Dict[str, Any]) -> str:
    """
    data MUST include:
    {
        "sub": user_id,
        "role": "donor | hospital | admin"
    }
    """

    return _create_token(
        data,
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "access"
    )


# =========================================================
# REFRESH TOKEN
# =========================================================

def create_refresh_token(data: Dict[str, Any]) -> str:
    return _create_token(
        data,
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        "refresh"
    )


# =========================================================
# VERIFY TOKEN
# =========================================================

def verify_token(token: str, expected_type: str = "access") -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # check token type
        if payload.get("type") != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        return payload

    except JWTError as e:
        logger.error(f"❌ Token error: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )


# =========================================================
# GET USER FROM TOKEN
# =========================================================

def get_user_from_token(token: str) -> Dict[str, Any]:
    payload = verify_token(token)

    user_id = payload.get("sub")
    role = payload.get("role")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    return {
        "user_id": int(user_id),
        "role": role
    }


# =========================================================
# FASTAPI DEPENDENCY (VERY IMPORTANT)
# =========================================================

security_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
):
    token = credentials.credentials
    return get_user_from_token(token)


# =========================================================
# PASSWORD STRENGTH
# =========================================================

def validate_password_strength(password: str) -> bool:
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        return False

    return all([
        any(c.isupper() for c in password),
        any(c.islower() for c in password),
        any(c.isdigit() for c in password),
        any(c in "!@#$%^&*()-_=+" for c in password)
    ])


# =========================================================
# SECURITY HEALTH CHECK
# =========================================================

def security_health_check() -> dict:
    return {
        "jwt_algorithm": settings.ALGORITHM,
        "access_token_expiry": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "refresh_token_expiry_days": settings.REFRESH_TOKEN_EXPIRE_DAYS,
        "password_hashing": "bcrypt",
        "security_status": "ACTIVE",
        "roles_supported": ["donor", "hospital", "admin"]
    }