from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AutoParts Quoter API"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    OPENAI_API_KEY: str
    LLM_MODEL: str = "gpt-4o-mini"
    WAHA_BASE_URL: str
    WAHA_TOKEN: str
    WAHA_DEFAULT_SENDER: str
    FRONTEND_URL: str = "http://localhost:3000"
    class Config:
        env_file = ".env"

settings = Settings()
