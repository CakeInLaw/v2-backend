from enum import IntEnum, StrEnum
from typing import TypeVar

from core.schemas.models.columns import EnumSchema
from core.utils import import_string
from ._base import ColumnValidator


__all__ = ["EnumValidator"]

ENUM = TypeVar('ENUM', IntEnum, StrEnum)


class EnumValidator(ColumnValidator[EnumSchema, ENUM]):

    def _post_init(self):
        self.python_type = import_string(f'enums.{self.schema.enum_type_name}')
        self.is_int_enum = issubclass(self.python_type, IntEnum)
        self.is_str_enum = issubclass(self.python_type, StrEnum)
        super()._post_init()

    def _transform(self, value: str | int | ENUM) -> ENUM:
        if isinstance(value, str):
            if self.is_int_enum:
                value = int(value)
            value = self.python_type(value)
        elif isinstance(value, int):
            if self.is_str_enum:
                value = str(value)
            value = self.python_type(value)
        return value
