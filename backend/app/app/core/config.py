import os

from pydantic import BaseSettings
import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Simple Task Tracker'
    VERSION: str = '0.1.1'
    DB_DRIVER: str = os.getenv('SQL_DRIVER')
    DB_URL: str = 'sqlite:///./sql_app.db' if DB_DRIVER == 'sqlite3' else ''
    TEST_DB_URL: str = 'sqlite:///test_sql_app.db' if DB_DRIVER == 'sqlite3' else ''
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 12
    SECRET_KEY: str = 'some_secret_key'  # openssl rand -hex 32


settings = Settings()
