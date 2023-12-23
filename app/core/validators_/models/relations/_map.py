from typing import TYPE_CHECKING, Type

from core.schemas.models.relations import R_SCH
from core.schemas import RelationTypes

from ._base import REL_VAL
from .forward import ForwardRelationValidator
from .reverse import ReverseRelationValidator

if TYPE_CHECKING:
    from .._base import M_VAL

__all__ = ["get_relation_validator"]


relation_validators_map: dict[RelationTypes, Type[REL_VAL]] = {
    RelationTypes.FK: ForwardRelationValidator,
    RelationTypes.O2O: ForwardRelationValidator,
    RelationTypes.REV_FK: ReverseRelationValidator,
    RelationTypes.REV_O2O: ReverseRelationValidator,
}


def get_relation_validator(schema: R_SCH, model_validator: "M_VAL") -> REL_VAL:
    return relation_validators_map[schema.type](schema, model_validator)
