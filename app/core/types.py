import enum
from typing import TypeVar
from uuid import UUID


__all__ = ["ENUM", "PK"]


ENUM = TypeVar('ENUM', bound=enum.IntEnum | enum.StrEnum)
PK = TypeVar('PK', int, str, UUID)
