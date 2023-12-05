from typing import TypeVar, Type

from core.db.models import MODEL
from ._base import RelationSchema, RelationSchemaGenerator, relation_schemas
from .._schema_generator import kw_property
from ..._enums import RelationTypes


__all__ = [
    "ReverseRelationSchema",
    "ReverseOneToOneRelationSchemaGenerator",
    "ReverseForeignKeyRelationSchemaGenerator",
]


RR_SCH = TypeVar("RR_SCH", bound="ReverseRelationSchema")


class ReverseRelationSchema(RelationSchema):
    local_remote_pairs: dict[str, str]


class ReverseRelationSchemaGenerator(RelationSchemaGenerator[RR_SCH, MODEL]):
    schema_cls: Type[RR_SCH] = ReverseRelationSchema

    @kw_property
    def read_only(self) -> bool:
        return self._rel.info.get('read_only', True)

    @kw_property
    def local_remote_pairs(self):
        return {
            local.key: remote.key
            for local, remote in self._rel.local_remote_pairs
        }


@relation_schemas.dispatch_for(RelationTypes.REV_O2O)
class ReverseOneToOneRelationSchemaGenerator(ReverseRelationSchemaGenerator[RR_SCH, MODEL]):
    _type = RelationTypes.REV_O2O


@relation_schemas.dispatch_for(RelationTypes.REV_FK)
class ReverseForeignKeyRelationSchemaGenerator(ReverseRelationSchemaGenerator[RR_SCH, MODEL]):
    _type = RelationTypes.REV_FK
