from typing import Generic, TypeVar, Any, TYPE_CHECKING, Type, Union

from core.schema import A_SCH

if TYPE_CHECKING:
    from core.repositories import M_REP, LIST_REP
    from ..models import M_VAL
    from .lists import LIST_VAL


__all__ = ["AttrValidator", "A_VAL", "AttrValidatorParent", "ParentRepository"]

T = TypeVar('T', bound=Any)
AttrValidatorParent = Type["M_VAL"] | "LIST_VAL"
ParentRepository = Union["M_REP", "LIST_REP"]


class AttrValidator(Generic[A_SCH, T]):
    def __init__(self, schema: A_SCH, parent: AttrValidatorParent):
        self.schema = schema
        self.parent = parent
        self._parent_is_list: bool = self.parent.is_list
        self._post_init()

    def _post_init(self):
        pass

    async def validate(self, value: T, repository: ParentRepository) -> None:
        raise NotImplementedError()

    async def transform(self, value: Any, repository: ParentRepository) -> T:
        raise NotImplementedError()

    def modify_model_validator(self):
        pass


A_VAL = TypeVar('A_VAL', bound=AttrValidator)
