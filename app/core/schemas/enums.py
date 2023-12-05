from typing import Type
from enum import IntEnum, StrEnum

from pydantic import BaseModel

from ._enums import EnumSubTypes


__all__ = ["EnumDescription", "collect_enums"]


class EnumDescription(BaseModel):
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


def collect_enums():
    import enums
    return [
        EnumDescription.from_type(v)
        for k, v in enums.__dict__.items()
        if isinstance(v, type) and issubclass(v, (IntEnum, StrEnum)) and v.__members__
    ]
