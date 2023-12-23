from typing import ClassVar, TypeVar

from pydantic import computed_field

from ._base import AttrSchema
from .._types import Attrs, Relations


__all__ = [
    "RelationSchema", "REL_SCH",
    "ForwardRelationSchema", "FWD_REL_SCH", "ForeignKeyRelationSchema", "OneToOneRelationSchema",
    "ReverseRelationSchema", "REV_REL_SCH", "ReverseForeignKeyRelationSchema", "ReverseOneToOneRelationSchema"
]


class RelationSchema(AttrSchema):
    _attr: ClassVar[Attrs] = Attrs.RELATION
    _type: ClassVar[Relations]

    to_model: str

    local_key: str
    remote_key: str

    @computed_field
    @property
    def type(self) -> Relations:
        return self._type


REL_SCH = TypeVar('REL_SCH', bound=RelationSchema)


class ForwardRelationSchema(RelationSchema):
    pass


FWD_REL_SCH = TypeVar('FWD_REL_SCH', bound=ForwardRelationSchema)


class ForeignKeyRelationSchema(ForwardRelationSchema):
    _type: ClassVar[Relations] = Relations.FK


class OneToOneRelationSchema(ForwardRelationSchema):
    _type: ClassVar[Relations] = Relations.O2O


class ReverseRelationSchema(RelationSchema):
    pass


REV_REL_SCH = TypeVar('REV_REL_SCH', bound=ReverseRelationSchema)


class ReverseForeignKeyRelationSchema(ReverseRelationSchema):
    _type: ClassVar[Relations] = Relations.REV_FK


class ReverseOneToOneRelationSchema(ReverseRelationSchema):
    _type: ClassVar[Relations] = Relations.REV_O2O
