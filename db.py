from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends


DATABASE_URL = "mysql://user:password@localhost/dbname"  # Zmienię to jak tylko ją stworzę
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
