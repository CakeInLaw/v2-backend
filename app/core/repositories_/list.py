from typing import Generic, Any, TypeVar, Type

from core.db.models import LIST_MODEL, OBJECT, ListModel
from core.db.connection import Session
from core.schemas.models import ListModelSchema
from core.validators_.models import ListModelValidator
from ._base import ModelRepository


__all__ = ["ListModelRepository", "LIST_REP"]

LIST_REP = TypeVar('LIST_REP', bound="ListModelRepository")


class ListModelRepository(
    ModelRepository[LIST_MODEL, ListModelValidator, ListModelSchema],
    Generic[LIST_MODEL, OBJECT]
):
    _validator_cls = ListModelValidator

    def __init__(self, session: Session, owner_instance: OBJECT):
        super().__init__(session=session)
        self.owner_instance = owner_instance

    @classmethod
    def bind(cls: Type[LIST_REP], model: Type[LIST_MODEL]) -> Type[LIST_REP]:
        assert issubclass(model, ListModel)
        name = model.__OWNER__.__full_name__ + model.__BACK_POPULATES__.title() + 'Repository'
        return type(name, (cls,), {'model': model})  # type: ignore

    async def get_list(self):
        ...

    async def create_list(self, data: list[dict[str, Any]]):
        ...

    async def add_row(self, data: dict[str, Any], rn: int = -1):
        ...

    async def rm_row(self, row_number: int):
        ...
