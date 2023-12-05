from enum import IntEnum, StrEnum
from typing import TypeVar

from core.schemas.models.columns import EnumSchema
from core.utils import import_string
from ._base import ColumnValidator


ENUM = TypeVar('ENUM', IntEnum, StrEnum)


class BooleanValidator(ColumnValidator[EnumSchema, ENUM]):

    def __init__(self, schema: EnumSchema):
        super().__init__(schema=schema)
        self.python_type = import_string(f'enums.{self._schema.enum_type_name}')
        self.is_int_enum = issubclass(self.python_type, IntEnum)
        self.is_str_enum = issubclass(self.python_type, StrEnum)

    def _transform(self, value: str | int | ENUM) -> ENUM:
        if isinstance(value, str):
            if self.is_int_enum:
                value = int(value)
            value = self.python_type(value)
        elif isinstance(value, int):
            if issubclass(self.python_type, StrEnum):
                value = str(value)
            value = self.python_type(value)
        return value
