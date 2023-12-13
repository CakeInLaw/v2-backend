from typing import Generic, TypeVar, Any, Type, cast, TYPE_CHECKING

from core.schemas.models import M_SCH
from ._attrs import A_VAL
from .columns import get_column_validator, COL_VAL
from .relations import get_relation_validator, REL_VAL
from .composites import get_composite_validator, COMP_VAL

if TYPE_CHECKING:
    from core.repositories import M_REP

__all__ = ["ModelValidator", "M_VAL"]

M_VAL = TypeVar('M_VAL', bound="ModelValidator")


class ModelValidatorMeta(type):
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        new_cls = cast(Type[M_VAL], super().__new__(mcs, name, bases, attrs))
        if 'schema' not in attrs:
            return new_cls

        schema = new_cls.schema

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
            col_validator.modify_model_validator()
        for rel_validator in relations.values():
            rel_validator.modify_model_validator()
        for comp_validator in composites.values():
            comp_validator.modify_model_validator()

        return new_cls


class ModelValidator(Generic[M_SCH], metaclass=ModelValidatorMeta):

    schema: M_SCH
    _columns: dict[str, COL_VAL]
    _relations: dict[str, REL_VAL]
    _composites: dict[str, COMP_VAL]

    available_attrs: dict[str, A_VAL]
    required_attrs: set[str]

    def __init__(self, repository: "M_REP"):
        self.repository = repository

    @classmethod
    def bind(cls: Type["M_VAL"], schema: M_SCH) -> Type["M_VAL"]:
        if hasattr(cls, 'schema'):
            raise Exception(f'{cls} is alteady bound')
        return type(f'{schema.name}{cls.__name__}', (cls, ), {'schema': schema})  # type: ignore

    @classmethod
    def get_available_attr(cls, name: str) -> A_VAL:
        return cls.available_attrs[name]

    @classmethod
    def get_attr(cls, name: str) -> A_VAL:
        if name in cls._columns:
            return cls._columns[name]
        if name in cls._relations:
            return cls._relations[name]
        if name in cls._composites:
            return cls._composites[name]
        raise ValueError(f'{name} is not attr of {cls.schema.namespace}.{cls.schema.name}')

    @classmethod
    def get_column(cls, name: str) -> COL_VAL:
        return cls._columns[name]

    @classmethod
    def get_relation(cls, name: str) -> REL_VAL:
        return cls._relations[name]

    @classmethod
    def get_composite(cls, name: str) -> COMP_VAL:
        return cls._composites[name]
