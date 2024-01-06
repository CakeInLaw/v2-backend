from typing import Generic, TypeVar

from core.schema import M_SCH
from .attrs import (
    A_VAL,
    ColumnValidator, get_column_validator,
    RelationValidator, get_relation_validator,
    CompositeValidator, get_composite_validator,
    PropertyValidator, get_property_validator
)


__all__ = ["ModelValidator", "M_VAL"]


class ModelValidator(Generic[M_SCH]):
    is_list: bool = False

    schema: M_SCH
    _columns: dict[str, ColumnValidator]
    _relations: dict[str, RelationValidator]
    _properties: dict[str, PropertyValidator]
    _composites: dict[str, CompositeValidator]

    available_attrs: dict[str, A_VAL]
    required_attrs: set[str]

    @classmethod
    def get_available_attr(cls, name: str) -> A_VAL:
        return cls.available_attrs[name]

    @classmethod
    def get_attr(cls, name: str) -> A_VAL:
        if name in cls._columns:
            return cls._columns[name]
        if name in cls._relations:
            return cls._relations[name]
        if name in cls._properties:
            return cls._properties[name]
        if name in cls._composites:
            return cls._composites[name]
        raise ValueError(f'{name} is not attr of {cls.schema.namespace}.{cls.schema.name}')

    @classmethod
    def get_column(cls, name: str) -> ColumnValidator:
        return cls._columns[name]

    @classmethod
    def get_relation(cls, name: str) -> RelationValidator:
        return cls._relations[name]

    @classmethod
    def get_property(cls, name: str) -> PropertyValidator:
        return cls._properties[name]

    @classmethod
    def get_composite(cls, name: str) -> CompositeValidator:
        return cls._composites[name]

    @classmethod
    def is_schema_bound(cls) -> bool:
        return getattr(cls, 'schema', None) is not None

    def __init_subclass__(cls, schema: M_SCH = None):
        if schema is None:
            return
        assert cls.is_schema_bound()

        cls.schema = schema
        cls._columns = {
            col_schema.name: get_column_validator(schema=col_schema, parent=cls)
            for col_schema in schema.get_columns()
        }
        cls._relations = {
            rel_schema.name: get_relation_validator(schema=rel_schema, parent=cls)
            for rel_schema in schema.get_relations()
        }
        cls._properties = {
            prop_schema.name: get_property_validator(schema=prop_schema, parent=cls)
            for prop_schema in schema.get_properties()
        }
        cls._composites = {
            comp_schema.name: get_composite_validator(schema=comp_schema, parent=cls)
            for comp_schema in schema.get_composites()
        }

        cls.available_attrs = {}
        cls.required_attrs = set()
        for col_validator in cls._columns.values():
            col_validator.modify_parent()
        for rel_validator in cls._relations.values():
            rel_validator.modify_parent()
        for prop_validator in cls._properties.values():
            prop_validator.modify_parent()
        for comp_validator in cls._composites.values():
            comp_validator.modify_parent()


M_VAL = TypeVar('M_VAL', bound=ModelValidator)
