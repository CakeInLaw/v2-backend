from typing import TypeVar, Generic, TYPE_CHECKING, Type

from core.schemas.models.composite import C_SCH

if TYPE_CHECKING:
    from ..models import MV

__all__ = ["CompositeValidator", "CompV"]

T = TypeVar('T')


class CompositeValidator(Generic[C_SCH, T]):
    def __init__(self, schema: C_SCH, model_validator: Type["MV"]):
        self._schema = schema
        self._model_validator = model_validator

    async def validate(self, value: T):
        raise NotImplementedError()

    def transform(self, value: T) -> T:
        raise NotImplementedError()

    def modify_model_validator(self):
        pass


CompV = TypeVar('CompV', bound=CompositeValidator)
