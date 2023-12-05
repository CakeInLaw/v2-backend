from typing import ClassVar

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from .db import DBConf


__all__ = ["Settings", "settings"]


class AppSettings(BaseModel):
    VERSION: str = '0.1.0'
    DEBUG: bool


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__')

    app: AppSettings
    db: DBConf

    entities: ClassVar[list[str]] = [
        'directories.users',
        'directories.employees',
    ]


settings = Settings(_env_file='.env')
