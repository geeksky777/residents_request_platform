from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://request_user:request_pass@localhost:5432/request_db"
    )
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9094"


settings = Settings()
