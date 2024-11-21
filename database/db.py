from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database setup
DATABASE_URL = os.getenv("HEROKU_POSTGRESQL_CHARCOAL_URL")  # Ensure this points to your local PostgreSQL database
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os



# # Database setup
# DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_engine(DATABASE_URL)

