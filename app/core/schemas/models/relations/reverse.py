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
    local_key: str
    remote_key: str


class ReverseRelationSchemaGenerator(RelationSchemaGenerator[RR_SCH, MODEL]):
    schema_cls: Type[RR_SCH] = ReverseRelationSchema

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert len(self._rel.local_remote_pairs) == 1

    @kw_property
    def read_only(self) -> bool:
        return self._rel.info.get('read_only', True)

    @kw_property
    def local_key(self):
        return self._rel.local_remote_pairs[0][0].key

    @kw_property
    def remote_key(self):
        return self._rel.local_remote_pairs[0][1].key


@relation_schemas.dispatch_for(RelationTypes.REV_O2O)
class ReverseOneToOneRelationSchemaGenerator(ReverseRelationSchemaGenerator[RR_SCH, MODEL]):
    _type = RelationTypes.REV_O2O


@relation_schemas.dispatch_for(RelationTypes.REV_FK)
class ReverseForeignKeyRelationSchemaGenerator(ReverseRelationSchemaGenerator[RR_SCH, MODEL]):
    _type = RelationTypes.REV_FK
