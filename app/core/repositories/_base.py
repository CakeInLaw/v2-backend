from abc import ABC, abstractmethod
from typing import Type, Any, Generic, TypeVar, Self

from core.schema import O_SCH, LIST_SCH
from core.validators import O_VAL, LIST_VAL
from .registry import get_repository, DEFAULT_REPOSITORY_KEY

__all__ = ["AbstractObjectRepository", "AbstractListRepository", "O_REP", "LIST_REP"]


ANY_MODEL = TypeVar('ANY_MODEL', bound=Any)
ANY_LIST = TypeVar('ANY_LIST', bound=Any)


class AbstractRepositoryMeta(type):
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        attrs.setdefault('related_map', {})
        super().__new__(mcs, name, bases, attrs)


class AbstractRepository:
    schema: O_SCH | LIST_SCH
    validator_cls: O_VAL | LIST_VAL
    related_map: dict[str, str]
    context: dict[str, Any]

    @property
    def validator(self) -> O_VAL:
        if not hasattr(self, '_validator_instance'):
            setattr(self, '_validator_instance', self.validator_cls(self))
        return getattr(self, '_validator_instance')

    def related(self, attr: str) -> "O_REP":
        for rel in self.schema.get_relations():
            if rel.name == attr:
                repo = get_repository(
                    name=rel.to_model,
                    variant=self.related_map.get(attr, DEFAULT_REPOSITORY_KEY),
                    raise_if_none=True,
                )
                return repo(context=self.context)
        raise ValueError(f'No relation with name "{attr}" found in schema "{self.schema.name}"')



class AbstractObjectRepository(ABC, Generic[ANY_MODEL, O_SCH, O_VAL], metaclass=AbstractRepositoryMeta):
    model: Type[ANY_MODEL]
    schema: O_SCH
    validator_cls: Type[O_VAL]
    related_map: dict[str, str]

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


O_REP = TypeVar('O_REP', bound=AbstractObjectRepository)


class AbstractListRepository(ABC, Generic[O_REP, ANY_LIST, LIST_SCH, LIST_VAL], metaclass=AbstractRepositoryMeta):
    model: Type[ANY_LIST]
    schema: LIST_SCH
    validator_cls: Type[LIST_VAL]
    related_map: dict[str, str]

    @abstractmethod
    def __init__(self, context: dict[str, Any], owner: O_REP):
        self.context = context
        self.owner = owner

    @abstractmethod
    async def get(self, **kwargs) -> list[ANY_LIST]: ...

    @abstractmethod
    async def add(self, **kwargs) -> None: ...

    @abstractmethod
    async def add_row(self, **kwargs) -> None: ...

    @abstractmethod
    async def clear(self, **kwargs) -> None: ...


LIST_REP = TypeVar('LIST_REP', bound=AbstractListRepository)
