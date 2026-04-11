from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     DB_HOST: str = "localhost"
#     DB_PORT: int = 5432
#     DB_USER: str = "request_user"
#     DB_PASSWORD: str = "request_pass"
#     DB_NAME: str = "request_db"

#     @property
#     def DATABASE_URL(self) -> str:
#         return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://request_user:request_pass@localhost:5432/request_db"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"

settings = Settings()
