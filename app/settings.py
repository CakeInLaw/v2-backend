from typing import ClassVar

from core.settings import BaseSettings
from core.db import DBConf


__all__ = ["Settings", "settings"]


class Settings(BaseSettings):
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


settings = Settings(_env_file='.env')
