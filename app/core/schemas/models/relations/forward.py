from typing import TypeVar, Type

from core.db.models import MODEL
from ._base import RelationSchema, RelationSchemaGenerator, relation_schemas
from .._schema_generator import kw_property
from ..._enums import RelationTypes


__all__ = [
    "ForwardRelationSchema",
    "OneToOneRelationSchemaGenerator",
    "ForeignKeyRelationSchemaGenerator"
]


FR_SCH = TypeVar("FR_SCH", bound="ForwardRelationSchema")


class ForwardRelationSchema(RelationSchema):
    local_remote_pairs: dict[str, str]


class ForwardRelationSchemaGenerator(RelationSchemaGenerator[FR_SCH, MODEL]):
    schema_cls: Type[FR_SCH] = ForwardRelationSchema

    @kw_property
    def read_only(self) -> bool:
        return self._rel.info.get('read_only', False)

    @kw_property
    def local_remote_pairs(self):
        return {
            local.key: remote.key
            for local, remote in self._rel.local_remote_pairs
        }


@relation_schemas.dispatch_for(RelationTypes.O2O)
class OneToOneRelationSchemaGenerator(ForwardRelationSchemaGenerator[FR_SCH, MODEL]):
    _type = RelationTypes.O2O


@relation_schemas.dispatch_for(RelationTypes.FK)
class ForeignKeyRelationSchemaGenerator(ForwardRelationSchemaGenerator[FR_SCH, MODEL]):
    _type = RelationTypes.FK
