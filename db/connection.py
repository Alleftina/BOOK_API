from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.config import SQLALCHEMY_DATABASE_URL

# Строка подключения к базе данных PostgreSQL

# Создание экземпляра класса Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создание экземпляра класса SessionLocal для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание экземпляра класса Base для определения моделей
Base = declarative_base()


def get_session():
    with SessionLocal() as session:
        yield session