from abc import ABC
from enum import IntEnum, StrEnum

from core.schema import EnumSchema, ENUM_SCH
from ._base import BaseSchemaCollector


__all__ = ["EnumSchemaCollector", "LocalEnumSchemaCollector"]


class EnumSchemaCollector(BaseSchemaCollector[ENUM_SCH], ABC):
    def add_in_schema(self, schema: ENUM_SCH):
        self.app_schema.add_enum(schema=schema)


class LocalEnumSchemaCollector(EnumSchemaCollector[ENUM_SCH]):
    def __iter__(self):
        import enums
        for k, v in enums.__dict__.items():
            if isinstance(v, type) and issubclass(v, (IntEnum, StrEnum)) and v.__members__:
                yield EnumSchema.from_type(v)
