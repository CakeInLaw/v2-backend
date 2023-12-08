from typing import TYPE_CHECKING, Type

from core.schemas.models.relations import R_SCH
from core.schemas import RelationTypes

from ._base import RV
from .forward import ForwardRelationValidator
from .reverse import ReverseRelationValidator

if TYPE_CHECKING:
    from ..models import MV

__all__ = ["get_relation_validator"]


relation_validators_map: dict[RelationTypes, Type[RV]] = {
    RelationTypes.FK: ForwardRelationValidator,
    RelationTypes.O2O: ForwardRelationValidator,
    RelationTypes.REV_FK: ReverseRelationValidator,
    RelationTypes.REV_O2O: ReverseRelationValidator,
}


def get_relation_validator(schema: R_SCH, model_validator: "MV") -> RV:
    return relation_validators_map[schema.type](schema, model_validator)
