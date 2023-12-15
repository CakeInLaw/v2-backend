from typing import TypeVar, Any, Generic, Type, cast

from sqlalchemy import select, Select, BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Object, MODEL
from core.schemas import get_model_schema
from core.schemas.models import M_SCH
from core.validators.models import M_VAL, ModelValidator
from ._registry import get_repository

__all__ = ["ModelRepository", "M_REP", "ModelRepositoryMeta"]

_O = TypeVar('_O', bound=Object)
M_REP = TypeVar('M_REP', bound="ModelRepository")


class ModelRepositoryMeta(type):
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        new_cls = cast(Type[M_REP], super().__new__(mcs, name, bases, attrs))
        if hasattr(new_cls, 'model'):
            new_cls.schema = get_model_schema(attrs['model'])
            new_cls._validator_cls = new_cls._validator_cls.bind(new_cls.schema)

            new_cls._relations = relations = {}
            for rel in new_cls.schema.relations:
                relations[rel.name] = (rel.to_model, 'default')
        return new_cls


class ModelRepository(Generic[MODEL, M_VAL, M_SCH], metaclass=ModelRepositoryMeta):
    model: Type[MODEL]
    _validator_cls: Type[M_VAL] = ModelValidator
    schema: M_SCH
    _relations: dict[str, tuple[str, str]]

    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def validator(self) -> M_VAL:
        if not hasattr(self, '_validator_instance'):
            setattr(self, '_validator_instance', self._validator_cls(self))
        return getattr(self, '_validator_instance')

    async def get_related(self, rel_name: str, pk: Any) -> _O:
        repo = get_repository(*self._relations[rel_name])(session=self.session)
        return await repo.get(pk)

    def _modify_check_unique_query(
            self,
            query: Select[tuple[MODEL]],
            attr_name: str,
            value: Any
    ) -> Select[tuple[MODEL]]:
        return query

    def _check_unique_whereclause(self, attr_name: str, value: Any) -> BinaryExpression[bool]:
        return cast(BinaryExpression[bool], getattr(self.model, attr_name) == value)

    async def check_unique(self, attr_name: str, value: Any) -> bool:
        query = select(self.model).where(self._check_unique_whereclause(attr_name=attr_name, value=value))
        query = self._modify_check_unique_query(query, attr_name, value)
        return not await self.session.scalar(select(query.exists()))
