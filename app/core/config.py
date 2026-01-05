from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "changethis"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GOOGLE_API_KEY: str

    # MongoDB
    MONGO_SERVER: str
    MONGO_PORT: int = 27017
    MONGO_DB: str
    MONGO_DATABASE_URI: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"

    def __init__(self, **values):
        super().__init__(**values)
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        if not self.MONGO_DATABASE_URI:
            self.MONGO_DATABASE_URI = f"mongodb://{self.MONGO_SERVER}:{self.MONGO_PORT}"

settings = Settings()
