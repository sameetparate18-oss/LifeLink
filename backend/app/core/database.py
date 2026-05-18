from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging

from app.core.config import settings

# =========================================================
# LOGGING
# =========================================================

logger = logging.getLogger("lifelink.database")
logging.basicConfig(level=settings.LOG_LEVEL)

# =========================================================
# BASE MODEL
# =========================================================

Base = declarative_base()

# =========================================================
# ENGINE (OPTIMIZED)
# =========================================================

engine = create_engine(
    settings.DATABASE_URL,

    # Connection Pool (important for production)
    poolclass=QueuePool,
    pool_size=getattr(settings, "DATABASE_POOL_SIZE", 10),
    max_overflow=getattr(settings, "DATABASE_MAX_OVERFLOW", 20),
    pool_pre_ping=True,
    pool_recycle=3600,

    # Debug mode
    echo=getattr(settings, "DATABASE_ECHO", False),

    # modern SQLAlchemy
    future=True
)

# =========================================================
# SESSION FACTORY
# =========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True
)

# =========================================================
# FASTAPI DEPENDENCY (MAIN USE)
# =========================================================

def get_db():
    """
    FastAPI dependency injection for DB session
    """
    db: Session = SessionLocal()

    try:
        yield db

    except SQLAlchemyError as e:
        logger.error(f"Database Error: {str(e)}")
        db.rollback()
        raise

    finally:
        db.close()

# =========================================================
# CONTEXT MANAGER (FOR SCRIPTS / BACKGROUND TASKS)
# =========================================================

@contextmanager
def db_session():
    """
    Used for scripts, background jobs, cron tasks
    NOT for FastAPI routes
    """
    db: Session = SessionLocal()

    try:
        yield db
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB Session Error: {str(e)}")
        raise

    finally:
        db.close()

# =========================================================
# HEALTH CHECK
# =========================================================

def check_database_connection() -> bool:
    """
    Verify DB connectivity
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
            logger.info("✅ Database connection successful")
            return True

    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        return False

# =========================================================
# INIT DATABASE
# =========================================================

def init_db():
    """
    Create all tables
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables initialized successfully")

    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {str(e)}")
        raise