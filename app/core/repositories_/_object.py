from typing import Any, TypeVar, Type, cast

from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from core.db.models import Model, OBJECT, LIST_MODEL, MODEL
from core.schemas.models import O_SCH
from core.validators_.models import O_VAL, ObjectValidator
from ._base import ModelRepository, ModelRepositoryMeta
from ._registry import register_repository
from .list import ListModelRepository, LIST_REP


__all__ = ["ObjectRepository", "O_REP"]

O_REP = TypeVar('O_REP', bound="ObjectRepository")


class ObjectRepositoryMeta(ModelRepositoryMeta):

    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        new_cls = cast(Type[O_REP], super().__new__(mcs, name, bases, attrs))
        if hasattr(new_cls, 'model'):
            new_cls._lists = lists = {}
            list_repo_map = new_cls._list_repository_cls_map
            default_list_repo_cls = list_repo_map['_']
            for list_schema in new_cls.schema.lists:
                attr_name = list_schema.owner_attr_name
                list_model = cast(Type[LIST_MODEL], Model.find(list_schema.namespace, list_schema.name))
                lists[attr_name] = list_repo_map.get(attr_name, default_list_repo_cls).bind(model=list_model)

            new_cls.pk_attr = pk_attr = new_cls.schema.primary_keys[0]
            new_cls.pk = property(lambda self: getattr(new_cls.model, pk_attr))
            register_repository(new_cls)
        return new_cls


class ObjectRepository(ModelRepository[OBJECT, O_VAL, O_SCH], metaclass=ObjectRepositoryMeta):
    _validator_cls: Type[O_VAL] = ObjectValidator
    _list_repository_cls_map = {'_': ListModelRepository}

    _lists: dict[str, Type[LIST_REP]]
    pk_attr: str
    pk: InstrumentedAttribute

    def __init__(self, session: AsyncSession, instance: OBJECT = None):
        super().__init__(session=session)
        self._instance: OBJECT | None = None
        if instance is None:
            self.clear_instance()
        else:
            self.bind_instance(instance)

    async def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self.validator.validate(data=data)

    async def transform_pk(self, pk: Any) -> Any:
        return await self.validator.transform_pk(value=pk)

    @property
    def current_instance(self) -> OBJECT | None:
        return getattr(self, '_instance', None)

    def clear_instance(self):
        self._instance = None

    def bind_instance(self, instance: OBJECT):
        self._instance = instance

    async def filter(self, filters) -> list[OBJECT]:
        ...

    async def get(self, pk: Any) -> OBJECT:
        pk = await self.validator.transform_pk(pk)
        return await self.session.scalar(select(self.model).where(self.pk == pk))

    async def create(self, data: dict[str, Any]) -> OBJECT:
        valid_data = await self.validate(data)
        instance = self.model(**valid_data)
        self.session.add(instance)
        return instance

    async def update(self, data: dict[str, Any]) -> OBJECT:
        instance = self.current_instance
        assert instance is not None
        valid_data = await self.validate(data)
        for attr, value in valid_data.items():
            setattr(instance, attr, value)
        return instance

    async def delete(self, pk: Any) -> None:
        ...

    def _modify_check_unique_query(
            self,
            query: Select[tuple[MODEL]],
            attr_name: str,
            value: Any
    ) -> Select[tuple[MODEL]]:
        if self.current_instance:
            query = query.where(self.pk != getattr(self.current_instance, self.pk_attr))
        return query
