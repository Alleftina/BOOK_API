from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
# Строка подключения к базе данных PostgreSQL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Создание экземпляра класса Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создание экземпляра класса SessionLocal для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание экземпляра класса Base для определения моделей
Base = declarative_base()
