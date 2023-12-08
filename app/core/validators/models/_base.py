from typing import Generic, TypeVar, Any, Type, cast, TYPE_CHECKING

from core.schemas.models import M_SCH
from ..columns import get_column_validator, CV
from ..relations import get_relation_validator, RV
from ..composites import get_composite_validator, CompV

if TYPE_CHECKING:
    from core.repositories import M_REP

__all__ = ["ModelValidator", "M_VAL"]


class ModelValidatorMeta(type):
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        new_cls = cast(Type[M_VAL], super().__new__(mcs, name, bases, attrs))
        if '_schema' not in attrs:
            return new_cls

        schema = new_cls._schema

        new_cls._columns = columns = {}
        for col_schema in schema.columns:
            columns[col_schema.name] = get_column_validator(schema=col_schema, model_validator=new_cls)

        new_cls._relations = relations = {}
        for rel_schema in schema.relations:
            relations[rel_schema.name] = get_relation_validator(schema=rel_schema, model_validator=new_cls)

        new_cls._composites = composites = {}
        for comp_schema in schema.composites:
            composites[comp_schema.name] = get_composite_validator(schema=comp_schema, model_validator=new_cls)

        new_cls.available_attrs = {}
        new_cls.required_attrs = set()
        for col_name, col_validator in columns.items():
            if col_validator.is_available():
                new_cls.available_attrs[col_name] = col_validator
                if col_validator.is_required():
                    new_cls.required_attrs.add(col_name)
        for rel_validator in relations.values():
            rel_validator.modify_model_validator()
        for comp_validator in composites.values():
            comp_validator.modify_model_validator()

        return new_cls


class ModelValidator(Generic[M_SCH], metaclass=ModelValidatorMeta):

    _schema: M_SCH
    _columns: dict[str, CV]
    _relations: dict[str, RV]
    _composites: dict[str, CompV]

    available_attrs: dict[str, CV | CompV]
    required_attrs: set[str]

    def __init__(self, repository: M_REP):
        self.repository = repository

    @classmethod
    def bind(cls: Type["M_VAL"], schema: M_SCH) -> Type["M_VAL"]:
        if hasattr(cls, '_schema'):
            raise Exception(f'{cls} is alteady bound')
        return type(f'{schema.name}{cls.__name__}', (cls, ), {'_schema': schema})  # type: ignore

    @classmethod
    def get_available_attr(cls, name: str) -> CV | CompV:
        return cls.available_attrs[name]

    @classmethod
    def get_attr(cls, name: str) -> CV | CompV:
        if name in cls._columns:
            return cls._columns[name]
        if name in cls._relations:
            return cls._relations[name]
        if name in cls._composites:
            return cls._composites[name]
        raise ValueError(f'{name} is not attr of {cls._schema.namespace}.{cls._schema.name}')

    @classmethod
    def get_column(cls, name: str) -> CV:
        return cls._columns[name]

    @classmethod
    def get_relation(cls, name: str):
        return cls._relations[name]

    @classmethod
    def get_composite(cls, name: str) -> CompV:
        return cls._composites[name]


M_VAL = TypeVar('M_VAL', bound=ModelValidator)
