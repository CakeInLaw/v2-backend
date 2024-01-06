from abc import ABC, abstractmethod
from typing import Type, Any, Generic, TypeVar, Self, cast

from core.schema import O_SCH, LIST_SCH
from core.validators import O_VAL, LIST_VAL
from .registry import get_repository, DEFAULT_REPOSITORY_KEY


__all__ = [
    "AbstractObjectRepository", "O_REP",
    "AbstractListRepository", "LIST_REP"
]


ANY_MODEL = TypeVar('ANY_MODEL', bound=Any)
ANY_LIST = TypeVar('ANY_LIST', bound=Any)


class AbstractRepository:
    schema: O_SCH | LIST_SCH
    validator_cls: Type[O_VAL | LIST_VAL]
    related_map: dict[str, str]
    context: dict[str, Any]

    @property
    def validator(self) -> O_VAL:
        if not hasattr(self, '_validator_instance'):
            setattr(self, '_validator_instance', self.validator_cls(self))
        return getattr(self, '_validator_instance')

    @classmethod
    def is_schema_bound(cls) -> bool:
        return getattr(cls, 'schema', None) is not None

    def related_repository(self, attr: str) -> "O_REP":
        for rel in self.schema.get_relations():
            if rel.name == attr:
                repo = get_repository(
                    name=rel.to_model,
                    variant=self.related_map[attr],
                    raise_if_none=True,
                )
                return repo(context=self.context)
        raise ValueError(f'No relation with name "{attr}" found in schema "{self.schema.name}"')

    def __init_subclass__(cls, schema: O_SCH | LIST_SCH = None):
        if schema is None:
            return
        assert not cls.is_schema_bound()
        cls.schema = schema
        if getattr(cls, 'related_map', None) is None:
            cls.related_map = {}
        for rel in schema.get_relations():
            cls.related_map.setdefault(rel.name, DEFAULT_REPOSITORY_KEY)


ABC_REP = TypeVar('ABC_REP', bound=AbstractRepository)


class AbstractObjectRepository(ABC, Generic[ANY_MODEL, O_SCH, O_VAL], AbstractRepository):
    model: Type[ANY_MODEL]
    schema: O_SCH
    validator_cls: Type[O_VAL]
    DEFAULT_LIST_REPOSITORY_CLS: Type["LIST_REP"]
    list_cls_map: dict[str, Type["LIST_REP"]]

    def __init__(self, context: dict[str, Any]):
        self.context = context

    def with_instance(self, instance: ANY_MODEL) -> Self:
        self.instance = instance
        return self

    @property
    def instance(self) -> ANY_MODEL:
        return getattr(self, '_instance', None)

    @instance.setter
    def instance(self, value: ANY_MODEL) -> None:
        assert value is not None
        setattr(self, '_instance', value)

    def clear_instance(self) -> None:
        assert getattr(self, '_instance', None) is not None
        setattr(self, '_instance', None)

    def __init_subclass__(cls, schema: O_SCH = None) -> None:
        super().__init_subclass__(schema=schema)
        if schema is None:
            return
        if getattr(cls, 'list_cls_map', None) is None:
            cls.list_cls_map = {}
        for list_schema in cls.schema.get_lists():
            list_schema_cls = cls.list_cls_map.get(list_schema.name, cls.DEFAULT_LIST_REPOSITORY_CLS)
            if getattr(list_schema_cls, 'model', None) is None:
                list_schema_cls = list_schema_cls.bind_model(cls._get_list_model(list_schema.name))
            cls.list_cls_map[list_schema.name] = list_schema_cls.bind_schema(schema=list_schema)

    @classmethod
    @abstractmethod
    def _get_list_model(cls, name: str) -> Any: ...

    def list_repository(self, name: str) -> "LIST_REP":
        return self.list_cls_map[name](context=self.context, owner=self)

    @classmethod
    def bind_model(cls: Type["O_REP"], model: Type[ANY_MODEL]) -> Type["O_REP"]:
        assert getattr(cls, 'model', None) is None
        return cast(Type["O_REP"], type(f'{model.__name__}Repository', (cls,), {'model': model}))

    @classmethod
    def bind_schema(cls: Type["O_REP"], schema: O_SCH) -> Type["O_REP"]:
        return cast(Type["O_REP"], type(f'{cls.__name__}Bound', (cls,), {}, schema=schema))

    @classmethod
    @abstractmethod
    def bind_schema_automatically(cls: Type["O_REP"]) -> Type["O_REP"]: ...

    @abstractmethod
    async def get(self, **kwargs) -> list[ANY_MODEL]: ...

    @abstractmethod
    async def get_one(self, pk: Any, **kwargs) -> ANY_MODEL | None: ...

    @abstractmethod
    async def get_many(self, pks: list, **kwargs) -> list[ANY_MODEL]: ...

    @abstractmethod
    async def create(self, data: dict[str, Any], **kwargs) -> ANY_MODEL: ...

    @abstractmethod
    async def update(self, data: dict[str, Any], **kwargs) -> ANY_MODEL: ...

    @abstractmethod
    async def delete(self, pk, **kwargs) -> None: ...

    @abstractmethod
    async def delete_many(self, pks, **kwargs) -> None: ...

    @abstractmethod
    async def is_unique(self, attr_name: str, value: Any) -> bool: ...

    # only for Documents. Others must raise error
    @abstractmethod
    async def conduct(self) -> None: ...


O_REP = TypeVar('O_REP', bound=AbstractObjectRepository)


class AbstractListRepository(ABC, Generic[O_REP, ANY_LIST, LIST_SCH, LIST_VAL], AbstractRepository):
    model: Type[ANY_LIST]
    schema: LIST_SCH
    validator_cls: Type[LIST_VAL]

    def __init__(self, context: dict[str, Any], owner: O_REP):
        self.context = context
        self.owner = owner

    @classmethod
    def bind_model(cls: Type["LIST_REP"], model: Type[ANY_LIST]) -> Type["LIST_REP"]:
        assert getattr(cls, 'model', None) is None
        return cast(Type["LIST_REP"], type(f'{model.__name__}ListRepository', (cls,), {'model': model}))

    @classmethod
    def bind_schema(cls: Type["LIST_REP"], schema: LIST_SCH) -> Type["LIST_REP"]:
        return cast(Type["LIST_REP"], type(f'{cls.__name__}Bound', (cls,), {}, schema=schema))

    @abstractmethod
    async def get(self, **kwargs) -> list[ANY_LIST]: ...

    @abstractmethod
    async def add(self, **kwargs) -> None: ...

    @abstractmethod
    async def add_row(self, **kwargs) -> None: ...

    @abstractmethod
    async def clear(self, **kwargs) -> None: ...


LIST_REP = TypeVar('LIST_REP', bound=AbstractListRepository)
