from typing import ClassVar

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.utils import import_string
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

    schema_collectors: ClassVar[list[str]] = [
        'core.schema_collectors.LocalEnumSchemaCollector',
        'core.schema_collectors.SaDirectorySchemaCollector',
        'core.schema_collectors.SaDocumentSchemaCollector',
    ]
    default_date_fmt: ClassVar[str] = '{dd}.{mm}.{YYYY}'
    default_datetime_fmt: ClassVar[str] = '{HH}:{MM}:{SS} {dd}.{mm}.{YYYY}'
    default_time_fmt: ClassVar[str] = '{HH}:{MM}:{SS}'


settings = Settings(_env_file='.env')
