from typing import Generator
from sqlalchemy.orm import Session
from src.config.db_dev import SessionLocal

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
