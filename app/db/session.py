import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core import config
from fastapi import Depends

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(
    "postgresql://postgres:727272@localhost:5432/ANWARSON DATA",  # Updated database URI
    echo=True  # Set echo to True to log all SQL statements
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    logger.info("Creating a new database session")
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        # Detailed error logging
        logger.error("An error occurred during the database session.")
        logger.error("Error type: %s", type(e).__name__)
        logger.error("Error details: %s", e)
        raise  # Reraise the exception after logging
    finally:
        db.close()
        logger.info("Database session closed")
