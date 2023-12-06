from typing import Type, TYPE_CHECKING

from core.schemas import CompositeTypes
from core.schemas.models.composite import C_SCH

from ._base import CompV
from .one_of import OneOfValidator

if TYPE_CHECKING:
    from ..models import MV


__all__ = ["get_composite_validator"]


composite_validators_map: dict[CompositeTypes, Type[CompV]] = {
    CompositeTypes.ONE_OF: OneOfValidator,
}


def get_composite_validator(schema: C_SCH, model_validator: MV) -> CompV:
    return composite_validators_map[schema.type](schema, model_validator)
