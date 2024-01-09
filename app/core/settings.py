from typing import ClassVar, cast

from pydantic import BaseModel
from pydantic_settings import BaseSettings as PydanticBaseSettings, SettingsConfigDict

from core.utils.lazy import LazyImport


__all__ = ["BaseSettings", "settings"]


class AppSettings(BaseModel):
    VERSION: str = '0.1.0'
    DEBUG: bool


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__')

    app: AppSettings

    entities: ClassVar[list[str]]
    schema_collectors: ClassVar[list[str]]

    default_date_fmt: ClassVar[str] = '{dd}.{mm}.{YYYY}'
    default_datetime_fmt: ClassVar[str] = '{HH}:{MM}:{SS} {dd}.{mm}.{YYYY}'
    default_time_fmt: ClassVar[str] = '{HH}:{MM}:{SS}'


settings = cast(BaseSettings, LazyImport('settings.settings'))
