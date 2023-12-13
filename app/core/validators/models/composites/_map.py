from typing import Type, TYPE_CHECKING

from core.schemas import CompositeTypes
from core.schemas.models.composite import C_SCH

from ._base import COMP_VAL
from .one_of import OneOfValidator

if TYPE_CHECKING:
    from .._base import M_VAL


__all__ = ["get_composite_validator"]


composite_validators_map: dict[CompositeTypes, Type[COMP_VAL]] = {
    CompositeTypes.ONE_OF: OneOfValidator,
}


def get_composite_validator(schema: C_SCH, model_validator: Type["M_VAL"]) -> COMP_VAL:
    return composite_validators_map[schema.type](schema, model_validator)
