from typing import TypeVar

from core.schemas.models import DirectorySchema
from ._object import ObjectValidator


__all__ = ["DirectoryValidator", "DIR_VAL"]

DIR_VAL = TypeVar('DIR_VAL', bound="DirectoryValidator")


class DirectoryValidator(ObjectValidator[DirectorySchema]):
    pass
