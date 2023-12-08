from typing import TypeVar, Generic, Any, TYPE_CHECKING, Type

from core.db import Model
from core.schemas.models.relations import R_SCH

if TYPE_CHECKING:
    from .._base import MV


__all__ = ["RelationValidator", "RV"]


class RelationValidator(Generic[R_SCH]):
    def __init__(self, schema: R_SCH, model_validator: Type["MV"]):
        self._schema = schema
        self._model_validator = model_validator
        self._to_model = Model.find_by_name(self._schema.to, raise_if_none=True)

    async def validate(self, value: Any):
        raise NotImplementedError()

    def transform(self, value: Any) -> Any:
        raise NotImplementedError()

    def modify_model_validator(self) -> None:
        pass


RV = TypeVar('RV', bound=RelationValidator)
