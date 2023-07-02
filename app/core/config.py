import os
from ast import literal_eval
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    db: str
    user: str
    password: str
    server: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.server}:5432/{self.db}"


@dataclass
class RedisConfig:
    host: str


@dataclass
class Env:
    database: DatabaseConfig
    redis: RedisConfig
    backend_cors_origins: list[str]

    @property
    def database_url(self) -> str:
        return self.database.url


def load_config():
    load_dotenv()

    database_config = DatabaseConfig(
        db=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        server=os.getenv("POSTGRES_SERVER"),
    )

    redis_config = RedisConfig(
        host=os.getenv("REDIS_HOST"),
    )

    backend_cors_origins = literal_eval(os.getenv("BACKEND_CORS_ORIGINS", "['*']"))

    return Env(
        database=database_config,
        redis=redis_config,
        backend_cors_origins=backend_cors_origins,
    )


env = load_config()
