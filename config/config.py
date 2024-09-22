from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Prefixes(BaseModel):
    prefix: str = "/api"


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = True
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="TEST_CONFIG__",
    )
    api: Prefixes = Prefixes()
    db: DataBaseConfig


settings = Settings()  # type: ignore
