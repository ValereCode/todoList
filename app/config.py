from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()