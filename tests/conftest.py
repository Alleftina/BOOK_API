import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from sqlalchemy_utils import database_exists, drop_database, create_database

from db.connection import Base

from main import app
from utils.config import DATABASE_URL_TEST


engine_test = create_engine(DATABASE_URL_TEST)
SessionLocal = sessionmaker(bind=engine_test)




@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test, checkfirst=True)


@pytest.fixture
def session(db):
    SessionLocal = sessionmaker(bind=engine_test)
    session = SessionLocal()
    yield session
    session.close()