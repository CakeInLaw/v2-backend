from typing import Generic, Type, TYPE_CHECKING, TypeVar, Any

from core.schema import A_SCH

if TYPE_CHECKING:
    from core.repositories import M_REP
    from ..models import M_VAL


__all__ = ["AttrValidator", "A_VAL"]

T = TypeVar('T')
A_VAL = TypeVar('A_VAL', bound="AttrValidator")


class AttrValidator(Generic[A_SCH, T]):
    def __init__(self, schema: A_SCH, model_validator: Type["M_VAL"]):
        self.schema = schema
        self.model_validator = model_validator
        self._post_init()

    def _post_init(self):
        pass

    async def validate(self, value: T, repository: "M_REP") -> None:
        raise NotImplementedError()

    async def transform(self, value: Any, repository: "M_REP") -> T:
        raise NotImplementedError()

    def modify_model_validator(self):
        pass
