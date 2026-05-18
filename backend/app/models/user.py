import uuid
from sqlalchemy import Boolean, Column, String, DateTime, func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    # -----------------------
    # PRIMARY KEY
    # -----------------------
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # -----------------------
    # BASIC INFO
    # -----------------------
    full_name = Column(String(100), nullable=False, index=True)

    email = Column(String(255), unique=True, nullable=False, index=True)

    phone = Column(String(20), unique=True, nullable=True, index=True)

    # -----------------------
    # SECURITY
    # -----------------------
    password_hash = Column(String(255), nullable=False)

    # -----------------------
    # USER ROLE SYSTEM
    # -----------------------
    role = Column(
        String(20),
        nullable=False,
        default="user",
        index=True
    )
    # roles: user | admin | hospital | donor (for LifeLink type apps)

    # -----------------------
    # STATUS FLAGS
    # -----------------------
    is_active = Column(Boolean, default=True)

    is_verified = Column(Boolean, default=False)

    is_deleted = Column(Boolean, default=False)

    # -----------------------
    # TIMESTAMPS (VERY IMPORTANT 🔥)
    # -----------------------
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )