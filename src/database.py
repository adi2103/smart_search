import logging

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from src.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Database dependency with error handling"""
    db = None
    try:
        db = SessionLocal()
        yield db
    except HTTPException:
        # Re-raise HTTP exceptions (don't convert to 500)
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    finally:
        if db:
            try:
                db.close()
            except Exception as e:
                logger.error(f"Error closing database connection: {e}")
