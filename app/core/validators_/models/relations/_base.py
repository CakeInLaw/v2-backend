from typing import TypeVar, cast, Type, Any

from core.schema import R_SCH
from .._attrs import AttrValidator, T

__all__ = ["RelationValidator", "REL_VAL"]

REL_VAL = TypeVar('REL_VAL', bound="RelationValidator")


class RelationValidator(AttrValidator[R_SCH, Any]):
    def transform(self, value: Any, repository: "M_REP") -> T:
