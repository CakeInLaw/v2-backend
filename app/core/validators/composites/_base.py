from typing import TypeVar, Generic, TYPE_CHECKING, Any

from core.schemas.models.composite import C_SCH

if TYPE_CHECKING:
    from ..models import MV

__all__ = ["CompositeValidator", "CompV"]

T = TypeVar('T')


class CompositeValidator(Generic[C_SCH, T]):
    def __init__(self, schema: C_SCH, model_validator: "MV"):
        self._schema = schema
        self._model_validator = model_validator

    def validate(self, value: dict[str, Any]):
        for col_name, col_value in value.items():
            self._model_validator.get_column(name=col_name).validate(value=value)

    def transform(self, value: T) -> dict[str, Any]:
        raise NotImplementedError()


CompV = TypeVar('CompV', bound=CompositeValidator)
