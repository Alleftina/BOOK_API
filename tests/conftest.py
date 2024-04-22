import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from models.models import metadata
from main import app
from utils.config import DATABASE_URL_TEST


engine_test = create_engine(DATABASE_URL_TEST)
SessionLocal = sessionmaker(bind=engine_test)
metadata.create_all(bind=engine_test)


@pytest.fixture(autouse=True, scope='function')
def db():
    metadata.create_all(bind=engine_test)
    yield
    metadata.drop_all(bind=engine_test)


@pytest.fixture
def session(db):
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def client():
    return TestClient(app)
