from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging

from app.core.config import settings


# =========================================================
# LOGGING CONFIGURATION
# =========================================================

logging.basicConfig(
    level=settings.LOG_LEVEL
)

logger = logging.getLogger("lifelink.database")


# =========================================================
# DATABASE ENGINE
# =========================================================

engine = create_engine(

    settings.DATABASE_URL,

    # Connection Pooling
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,

    # Performance
    pool_pre_ping=True,
    pool_recycle=3600,

    # Debug
    echo=settings.DATABASE_ECHO,

    # Future SQLAlchemy Style
    future=True
)


# =========================================================
# SESSION FACTORY
# =========================================================

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine,

    future=True
)


# =========================================================
# BASE MODEL
# =========================================================

Base = declarative_base()


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    except SQLAlchemyError as e:

        logger.error(
            f"Database Error: {str(e)}"
        )

        db.rollback()

        raise

    finally:

        db.close()


# =========================================================
# CONTEXT MANAGER
# =========================================================

@contextmanager
def db_session():

    db = SessionLocal()

    try:

        yield db

        db.commit()

    except Exception as e:

        db.rollback()

        logger.error(
            f"Session Rollback Error: {str(e)}"
        )

        raise

    finally:

        db.close()


# =========================================================
# DATABASE CONNECTION TEST
# =========================================================

def check_database_connection():

    try:

        with engine.connect() as connection:

            logger.info(
                "✅ Database connection successful"
            )

            return True

    except Exception as e:

        logger.error(
            f"❌ Database connection failed: {str(e)}"
        )

        return False


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

def init_db():

    try:

        Base.metadata.create_all(
            bind=engine
        )

        logger.info(
            "✅ Database tables initialized successfully"
        )

    except Exception as e:

        logger.error(
            f"❌ Failed to initialize database: {str(e)}"
        )

        raise