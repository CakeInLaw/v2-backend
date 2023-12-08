from typing import Type, TypeVar

from sqlalchemy.orm import RelationshipProperty, RelationshipDirection
from pydantic import BaseModel

from core.db.models import MODEL, Model, ListModel
from .._schema_generator import kw_property, BaseAttrSchemaGenerator, AttrSchemaGeneratorDispatcher
from ..._enums import RelationTypes


__all__ = ["RelationSchema", "RelationSchemaGenerator", "relation_schemas", "R_SCH"]


R_SCH = TypeVar("R_SCH", bound="RelationSchema")
R_GEN = TypeVar("R_GEN", bound="RelationSchemaGenerator")


class RelationSchema(BaseModel):
    name: str
    type: RelationTypes
    to: str
    read_only: bool


class RelationSchemaGenerator(BaseAttrSchemaGenerator[R_SCH, MODEL, RelationshipProperty]):
    _type: RelationTypes
    schema_cls: Type[RelationSchema]

    @property
    def _rel(self):
        return self._attr

    @kw_property
    def name(self) -> str:
        return self._rel.key

    @kw_property
    def type(self) -> RelationTypes:
        return self._type

    @kw_property
    def to(self):
        return Model.find_by_table(self._attr.target).__full_name__

    @kw_property
    def read_only(self) -> bool:
        raise NotImplementedError()


class RelationSchemaGeneratorDispatcher(
    AttrSchemaGeneratorDispatcher[R_GEN, RelationTypes, RelationshipProperty]
):
    def should_reg_by_type(self, type_):
        return isinstance(type_, RelationTypes)

    def _dispatch_by_attr(self, model: Type[MODEL], attr: RelationshipProperty) -> Type[R_GEN] | None:
        match attr.direction:
            case RelationshipDirection.ONETOMANY:
                if attr.uselist:
                    rel_model = Model.find_by_table(attr.target)
                    if issubclass(rel_model, ListModel):
                        # ObjectSchema.lists is set inside schema in lists attribute
                        return
                    rel_type = RelationTypes.REV_FK
                else:
                    rel_type = RelationTypes.REV_O2O
            case RelationshipDirection.MANYTOONE:
                local_columns = list(attr.local_columns)
                if len(local_columns) != 1:
                    raise RuntimeError('Unhandled situation')
                if local_columns[0].unique:
                    rel_type = RelationTypes.O2O
                else:
                    if issubclass(model, ListModel) and Model.find_by_table(attr.target) is model.__OWNER__:
                        # ListModelSchema.owner is set inside it`s schema
                        return
                    rel_type = RelationTypes.FK
            case RelationshipDirection.MANYTOMANY:
                raise RuntimeError('m2m relation is not supported now')
            case _:
                raise ValueError('Unhandled condition')
        return self._reg_map[rel_type]


relation_schemas = RelationSchemaGeneratorDispatcher()
