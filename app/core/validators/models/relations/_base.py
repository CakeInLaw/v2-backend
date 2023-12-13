from typing import TypeVar, cast, Type

from core.db import Model
from core.db.models import OBJECT
from core.schemas.models.relations import R_SCH
from .._attrs import AttrValidator


__all__ = ["RelationValidator", "REL_VAL"]

REL_VAL = TypeVar('REL_VAL', bound="RelationValidator")


class RelationValidator(AttrValidator[R_SCH, OBJECT]):

    def _post_init(self):
        self._to_model: Type[OBJECT] = Model.find_by_name(self.schema.to_model, raise_if_none=True)
