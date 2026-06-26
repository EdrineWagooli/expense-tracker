# Sets up the connection/engine to SQLite, nothing about what data looks like or how it's queried

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from contextlib import contextmanager

from models import Base


engine = create_engine('sqlite:///expense_tracker.db', echo=False)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

@contextmanager
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()