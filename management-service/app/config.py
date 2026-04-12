from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://management_user:management_pass@localhost:5433/management_db"
    )
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9094"


settings = Settings()
