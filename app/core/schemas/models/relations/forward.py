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
    local_key: str
    remote_key: str


class ForwardRelationSchemaGenerator(RelationSchemaGenerator[FR_SCH, MODEL]):
    schema_cls: Type[FR_SCH] = ForwardRelationSchema

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert len(self._rel.local_remote_pairs) == 1

    @kw_property
    def read_only(self) -> bool:
        return self._rel.info.get('read_only', False)

    @kw_property
    def local_key(self):
        return self._rel.local_remote_pairs[0][0].key

    @kw_property
    def remote_key(self):
        return self._rel.local_remote_pairs[0][1].key


@relation_schemas.dispatch_for(RelationTypes.O2O)
class OneToOneRelationSchemaGenerator(ForwardRelationSchemaGenerator[FR_SCH, MODEL]):
    _type = RelationTypes.O2O


@relation_schemas.dispatch_for(RelationTypes.FK)
class ForeignKeyRelationSchemaGenerator(ForwardRelationSchemaGenerator[FR_SCH, MODEL]):
    _type = RelationTypes.FK
