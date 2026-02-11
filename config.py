
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev")
    MAX_PALLETS: int = 26

settings = Settings()
