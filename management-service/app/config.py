from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     DB_HOST: str = "localhost"
#     DB_PORT: int = 5433
#     DB_USER: str = "management_user"
#     DB_PASSWORD: str = "management_pass"
#     DB_NAME: str = "management_db"

#     @property
#     def DATABASE_URL(self) -> str:
#         return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://management_user:management_pass@localhost:5433/management_db"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"

settings = Settings()
