import enum
from typing import TypeVar


__all__ = ["ENUM"]


ENUM = TypeVar('ENUM', bound=enum.IntEnum | enum.StrEnum)
