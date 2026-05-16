from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
import logging
import secrets

from app.core.config import settings


# =========================================================
# LOGGING CONFIGURATION
# =========================================================

logging.basicConfig(
    level=settings.LOG_LEVEL
)

logger = logging.getLogger("lifelink.security")


# =========================================================
# PASSWORD HASHING CONFIGURATION
# =========================================================

pwd_context = CryptContext(

    schemes=["bcrypt"],

    deprecated="auto",

    bcrypt__rounds=12
)


# =========================================================
# PASSWORD UTILITIES
# =========================================================

def hash_password(password: str) -> str:

    """
    Hash a plain password securely.
    """

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    """
    Verify plain password against hash.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================================================
# ACCESS TOKEN CREATION
# =========================================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:

    """
    Create JWT access token.
    """

    to_encode = data.copy()

    if expires_delta:

        expire = datetime.utcnow() + expires_delta

    else:

        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # JWT PAYLOAD

    to_encode.update({
        "exp": expire,
        "type": "access",
        "iat": datetime.utcnow(),
        "jti": secrets.token_hex(16)
    })

    encoded_jwt = jwt.encode(

        to_encode,

        settings.SECRET_KEY,

        algorithm=settings.ALGORITHM
    )

    logger.info(
        "✅ Access token created successfully"
    )

    return encoded_jwt


# =========================================================
# REFRESH TOKEN CREATION
# =========================================================

def create_refresh_token(
    data: Dict[str, Any]
) -> str:

    """
    Create refresh JWT token.
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "iat": datetime.utcnow(),
        "jti": secrets.token_hex(16)
    })

    refresh_token = jwt.encode(

        to_encode,

        settings.SECRET_KEY,

        algorithm=settings.ALGORITHM
    )

    logger.info(
        "✅ Refresh token created successfully"
    )

    return refresh_token


# =========================================================
# TOKEN VERIFICATION
# =========================================================

def verify_token(
    token: str
) -> Dict[str, Any]:

    """
    Verify and decode JWT token.
    """

    try:

        payload = jwt.decode(

            token,

            settings.SECRET_KEY,

            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError as e:

        logger.error(
            f"❌ Invalid token: {str(e)}"
        )

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid or expired token",

            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


# =========================================================
# GET CURRENT USER ID
# =========================================================

def get_user_id_from_token(
    token: str
) -> Optional[int]:

    """
    Extract user ID from token.
    """

    try:

        payload = verify_token(token)

        user_id = payload.get("sub")

        if user_id is None:

            return None

        return int(user_id)

    except Exception:

        return None


# =========================================================
# PASSWORD STRENGTH VALIDATION
# =========================================================

def validate_password_strength(
    password: str
) -> bool:

    """
    Validate password security.
    """

    if len(password) < settings.PASSWORD_MIN_LENGTH:

        return False

    has_upper = any(c.isupper() for c in password)

    has_lower = any(c.islower() for c in password)

    has_digit = any(c.isdigit() for c in password)

    special_characters = "!@#$%^&*()-_=+"

    has_special = any(
        c in special_characters
        for c in password
    )

    return all([
        has_upper,
        has_lower,
        has_digit,
        has_special
    ])


# =========================================================
# SECURITY HEALTH CHECK
# =========================================================

def security_health_check() -> dict:

    """
    Security system diagnostics.
    """

    return {

        "jwt_algorithm": settings.ALGORITHM,

        "token_expiry_minutes":
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,

        "password_hashing": "bcrypt",

        "security_status": "ACTIVE"
    }