import os

from pydantic import BaseSettings
import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    db_driver: str = os.getenv('SQL_DRIVER')
    db_url: str = 'sqlite:///./sql_app.db' if db_driver == 'sqlite3' else ''


settings = Settings()
