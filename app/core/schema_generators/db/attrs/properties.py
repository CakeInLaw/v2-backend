import uuid
import enum
import types
from inspect import getfullargspec
from typing import TypeVar, Type, get_origin, get_args
from decimal import Decimal
from datetime import date, time, datetime

from sqlalchemy.orm import QueryableAttribute
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.models import MODEL
from core.schema.attrs import PROP_SCH, PropertySchema, _constraints as constr
from ._base import AttrSchemaGenerator
from ._dispatcher import AttrSchemaGeneratorDispatcher
from ...gen_property import gen_property


__all__ = [
    "PropertySchemaGenerator", "PROP_GEN",
    "PropertySchemaGeneratorDispatcher", "property_schema_generators",
]


class PropertySchemaGenerator(AttrSchemaGenerator[PROP_SCH, QueryableAttribute]):
    schema_cls = PropertySchema
    _type_map: dict[type, constr.C] = {
        bool: constr.BooleanConstraint,
        date: constr.DateConstraint,
        datetime: constr.DateTimeConstraint,
        enum.IntEnum: constr.EnumConstraint,
        enum.StrEnum: constr.EnumConstraint,
        uuid.UUID: constr.GuidConstraint,
        int: constr.IntegerConstraint,
        Decimal: constr.NumericConstraint,
        str: constr.StringConstraint,
        time: constr.TimeConstraint,
    }

    @property
    def _prop(self) -> hybrid_property:
        if isinstance(self._attr, QueryableAttribute):
            return self._attr.descriptor
        return self._attr

    @gen_property
    def name(self) -> str:
        return self._prop.__name__

    @classmethod
    def register_constraint_type(cls, t: type, constraint: constr.C):
        cls._type_map[t] = constraint

    @classmethod
    def _prop_constraints(cls, t: type, **kwargs) -> constr.C:
        for base in t.__mro__:
            if base in cls._type_map:
                return cls._type_map[base](**kwargs)
        raise ValueError(f'{t} is not registered')

    @gen_property
    def required(self):
        return self._prop.info['required']

    @gen_property
    def nullable(self) -> bool | None:
        if self._prop.info['writeable'] and self._prop.fset:
            value_type = getfullargspec(self._prop.fset).annotations['value']
            return get_origin(value_type) is types.UnionType and types.NoneType in get_args(value_type)

    @gen_property
    def getter_constraints(self) -> constr.C | None:
        if self._prop.info['readable'] and self._prop.fget:
            fget_annotations = getfullargspec(self._prop.fget).annotations
            assert 'return' in fget_annotations, f'{self.owner.name}.{self.name} hasn`t "return" annotation'
            return self._prop_constraints(fget_annotations['return'], **self._prop.info['getter'])

    @gen_property
    def setter_constraints(self) -> constr.C | None:
        if self._prop.info['writeable'] and self._prop.fset:
            fset_annotations = getfullargspec(self._prop.fset).annotations
            assert 'value' in fset_annotations, f'{self.owner.name}.{self.name} hasn`t "value" annotation'
            return self._prop_constraints(fset_annotations['value'], **self._prop.info['setter'])


PROP_GEN = TypeVar('PROP_GEN', bound=PropertySchemaGenerator)


class PropertySchemaGeneratorDispatcher(AttrSchemaGeneratorDispatcher[PROP_GEN, hybrid_property, QueryableAttribute]):
    def should_reg_by_type(self, type_: QueryableAttribute | Type[MODEL]):
        return isinstance(type_, (QueryableAttribute, hybrid_property))

    def _dispatch_by_attr(self, model: Type[MODEL], attr: QueryableAttribute) -> Type[PROP_GEN] | None:
        return PropertySchemaGenerator

    def get_attr_name(self, attr: hybrid_property) -> str:
        return attr.__name__


property_schema_generators = PropertySchemaGeneratorDispatcher()
