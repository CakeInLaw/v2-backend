from typing import ClassVar, Any, Type, TypeVar, cast, Literal

from sqlalchemy import Table, event
from sqlalchemy.orm import DeclarativeBase, Mapper, declared_attr

from core.utils import camel_to_snake, default_if_none, classproperty

__all__ = ["Model", "MODEL", "get_base_metadata"]


class Model(DeclarativeBase):
    __table_args_extra__: dict[str, Any] = None

    __SCHEMA__: ClassVar[str]
    available_namespaces = frozenset(('directories', 'documents'))

    @declared_attr.directive
    @classmethod
    def __tablename__(cls):
        return camel_to_snake(cls.__name__) + 's'

    @declared_attr.directive
    @classmethod
    def __table_args__(cls):
        return {'schema': cls._get_schema_name(), **(default_if_none(cls.__table_args_extra__, dict, is_factory=True))}

    @classmethod
    def _get_schema_name(cls) -> str:
        return cls.__SCHEMA__

    @classmethod
    def find_by_table(cls, table: Table) -> Type["Model"]:
        return cls.find(table.schema, table.name)

    @classmethod
    def find_by_name(cls, name: str, raise_if_none: bool = False) -> Type["MODEL"]:
        schema_name, _, table_name = name.partition('.')
        return cls.find(schema_name, table_name, raise_if_none=raise_if_none)

    @classmethod
    def find(cls, schema_name: str, table_name: str, raise_if_none: bool = False) -> Type["Model"]:
        assert schema_name in cls.available_namespaces
        model = _models.get((schema_name, table_name))
        if raise_if_none and model is None:
            raise ValueError(f'No model {schema_name}.{table_name}')
        return model

    @classmethod
    def iter_models(cls, namespace: Literal["directories", "documents"] = None):
        if namespace:
            assert namespace in cls.available_namespaces
            return filter(lambda x: x[0][0] == namespace, _models.items())
        return _models.items()

    @classproperty
    def __namespace__(cls) -> str:
        return cast(Table, cls.__table__).schema

    @classproperty
    def __table__name__(cls) -> str:
        return cast(Table, cls.__table__).name

    @classproperty
    def __full_name__(cls) -> str:
        return f'{cls.__namespace__}.{cls.__table__name__}'


def get_base_metadata(*, init_first: bool = False):
    if init_first:
        from core.db import init_models
        init_models()
    return Model.metadata


MODEL = TypeVar('MODEL', bound=Model)

_models: dict[tuple[str, str], Type[MODEL]] = {}


@event.listens_for(Model, 'after_mapper_constructed', propagate=True)
def receive_after_mapper_constructed(_: Mapper, class_: Type[MODEL]):
    """Add model to _models to find it by schema_name and table_name"""
    table = cast(Table, class_.__table__)
    assert table.schema in Model.available_namespaces, f'"{table.schema}" schema name is not available'
    _models[(table.schema, table.name)] = class_
