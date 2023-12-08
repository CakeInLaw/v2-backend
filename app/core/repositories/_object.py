from typing import Any, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import OBJECT
from core.schemas.models import O_SCH
from core.validators.models import OV
from ._base import ModelRepository


__all__ = ["ObjectRepository", "O_REP"]


class ObjectRepository(ModelRepository[OBJECT, OV, O_SCH]):

    def __init__(self, session: AsyncSession, instance: OBJECT = None):
        super().__init__(session=session)
        self._instance = instance

    @property
    def current_instance(self) -> OBJECT | None:
        return getattr(self, '_instance', None)

    async def bind_instance(self, instance: OBJECT):
        self._instance = instance

    def filter(self, filter_data) -> list[OBJECT]:
        ...

    def get(self, pk: Any) -> OBJECT:
        ...

    def create(self, data: dict[str, Any]) -> OBJECT:
        ...

    def update(self, data: dict[str, Any]) -> OBJECT:
        ...

    def delete(self, pk: Any) -> None:
        ...


O_REP = TypeVar('O_REP', bound=ObjectRepository)
