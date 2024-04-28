from os import environ
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings():    
    # Postgres
    POSTGRES_USER: str = environ.get("POSTGRES_USER", 'postgres')
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", 'localhost')
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = environ.get("POSTGRES_DB", "postgres")
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", 'admin')
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # API
    API_IMAGEKIT_ID: str = environ.get("API_IMAGEKIT_ID")
    API_IMAGEKIT_SECRET: str = environ.get("API_IMAGEKIT_SECRET")
    API_IMAGEKIT_ENDPOINT: str = environ.get("API_IMAGEKIT_ENDPOINT")
    API_OCR_SPACE: str = environ.get("API_OCR_SPACE")
    API_DISCOGS_TOKEN: str = environ.get("API_DISCOGS_TOKEN")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
