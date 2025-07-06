from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path=".env")

class Config:
    DB_HOST = getenv("DB_HOST")
    SECRET_KEY = getenv("SECRET_KEY")
    ALGORITHM = getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")