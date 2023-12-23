from typing import Type, TypeVar
from enum import IntEnum, StrEnum

from pydantic import BaseModel

from ._types import EnumSubTypes


__all__ = ["EnumSchema", "ENUM_SCH"]


class EnumSchema(BaseModel):
    name: str
    type: EnumSubTypes
    values: dict[str, int] | dict[str, str]

    @classmethod
    def from_type(cls, enum_type: Type[IntEnum] | Type[StrEnum]):
        return cls.model_construct(
            name=enum_type.__name__,
            type=EnumSubTypes.INTEGER if issubclass(enum_type, IntEnum) else EnumSubTypes.STRING,
            values={value.name: value.value for value in enum_type.__members__.values()},
        )


ENUM_SCH = TypeVar('ENUM_SCH', bound=EnumSchema)
