from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DB_PASSWORD_TEST = os.getenv("DB_PASSWORD_TEST")
DB_USER_TEST = os.getenv("DB_USER_TEST")
DB_HOST_TEST = os.getenv("DB_HOST_TEST")
DB_NAME_TEST = os.getenv("DB_NAME_TEST")

NGROK_TOKEN = os.getenv("NGROK_TOKEN")
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DATABASE_URL_TEST = f"postgresql://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"
