from typing import TypeVar, Type

from sqlalchemy.orm import RelationshipProperty, RelationshipDirection

from core.db import Model
from core.db.models import MODEL, ListModel
from core.schema import Relations
from core.schema.attrs import (
    RelationSchema, REL_SCH,
    ForwardRelationSchema, FWD_REL_SCH, ForeignKeyRelationSchema, OneToOneRelationSchema,
    ReverseRelationSchema, REV_REL_SCH, ReverseForeignKeyRelationSchema, ReverseOneToOneRelationSchema
)
from ._base import AttrSchemaGenerator
from ._dispatcher import AttrSchemaGeneratorDispatcher
from ...gen_property import gen_property


__all__ = [
    "RelationSchemaGenerator", "REL_GEN", "RelationSchemaGeneratorDispatcher", "relation_schema_generators",
    "ForwardRelationSchemaGenerator",
    "ForeignKeyRelationSchemaGenerator", "OneToOneRelationSchemaGenerator",
    "ReverseRelationSchemaGenerator",
    "ReverseForeignKeyRelationSchemaGenerator", "ReverseOneToOneRelationSchemaGenerator",
]


class RelationSchemaGenerator(AttrSchemaGenerator[REL_SCH, RelationshipProperty]):
    schema_cls = RelationSchema

    @property
    def _rel(self):
        return self._attr

    @gen_property
    def name(self) -> str:
        return self._rel.key

    @gen_property
    def to_model(self) -> str:
        return Model.find_by_table(self._attr.target).__full_name__

    @gen_property
    def local_key(self) -> str:
        return self._rel.local_remote_pairs[0][0].key

    @gen_property
    def remote_key(self) -> str:
        return self._rel.local_remote_pairs[0][1].key


REL_GEN = TypeVar('REL_GEN', bound=RelationSchemaGenerator)


class RelationSchemaGeneratorDispatcher(AttrSchemaGeneratorDispatcher[REL_GEN, Relations, RelationshipProperty]):
    def _dispatch_by_attr(self, model: Type[MODEL], attr: RelationshipProperty) -> Type[REL_GEN] | None:
        match attr.direction:
            case RelationshipDirection.ONETOMANY:
                if attr.uselist:
                    rel_model = Model.find_by_table(attr.target)
                    if issubclass(rel_model, ListModel):
                        # ObjectSchema.lists is set inside schema in lists attribute
                        return
                    rel_type = Relations.REV_FK
                else:
                    rel_type = Relations.REV_O2O
            case RelationshipDirection.MANYTOONE:
                local_columns = list(attr.local_columns)
                if len(local_columns) != 1:
                    raise RuntimeError('Unhandled situation')
                if local_columns[0].unique:
                    rel_type = Relations.O2O
                else:
                    if issubclass(model, ListModel) and Model.find_by_table(attr.target) is model.__OWNER__:
                        # ListModelSchema.owner is set inside it`s schema
                        return
                    rel_type = Relations.FK
            case RelationshipDirection.MANYTOMANY:
                raise RuntimeError('m2m relation is not supported now')
            case _:
                raise ValueError('Unhandled condition')
        return self._reg_map[rel_type]


relation_schema_generators = RelationSchemaGeneratorDispatcher()


class ForwardRelationSchemaGenerator(RelationSchemaGenerator[FWD_REL_SCH]):
    schema_cls = ForwardRelationSchema


@relation_schema_generators.dispatch_for(Relations.FK)
class ForeignKeyRelationSchemaGenerator(ForwardRelationSchemaGenerator[ForeignKeyRelationSchema]):
    schema_cls = ForeignKeyRelationSchema


@relation_schema_generators.dispatch_for(Relations.O2O)
class OneToOneRelationSchemaGenerator(ForwardRelationSchemaGenerator[OneToOneRelationSchema]):
    schema_cls = OneToOneRelationSchema


class ReverseRelationSchemaGenerator(RelationSchemaGenerator[REV_REL_SCH]):
    schema_cls = ReverseRelationSchema


class ReverseForeignKeyRelationSchemaGenerator(ReverseRelationSchemaGenerator[ReverseForeignKeyRelationSchema]):
    schema_cls = ReverseForeignKeyRelationSchema


class ReverseOneToOneRelationSchemaGenerator(ReverseRelationSchemaGenerator[ReverseOneToOneRelationSchema]):
    schema_cls = ReverseOneToOneRelationSchema
