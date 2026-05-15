import uuid

from sqlalchemy import Boolean, Column, String

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    full_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    phone = Column(String, unique=True, nullable=True)

    password_hash = Column(String, nullable=False)

    role = Column(String, nullable=False)

    is_verified = Column(Boolean, default=False)