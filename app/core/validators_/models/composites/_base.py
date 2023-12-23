from typing import TypeVar

from core.schemas.models.composite import C_SCH
from .._attrs import AttrValidator


__all__ = ["CompositeValidator", "COMP_VAL"]

T = TypeVar('T')
COMP_VAL = TypeVar('COMP_VAL', bound="CompositeValidator")


class CompositeValidator(AttrValidator[C_SCH, T]):
    pass
