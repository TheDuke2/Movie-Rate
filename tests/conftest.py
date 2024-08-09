import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.ext.declarative import declarative_base

from app.models import Base  # Assuming models are using SQLAlchemy's Base
from fastapi.testclient import TestClient
from main import app  # Assuming you have a FastAPI app in main.py

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        clear_mappers()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    return TestClient(app)
