from typing import TypeVar, ClassVar

from pydantic import BaseModel

from .attrs import A_SCH, COL_SCH, REL_SCH, COMP_SCH, PROP_SCH, LIST_SCH
from ._types import Attrs


__all__ = [
    "ModelSchema", "ObjectSchema", "DirectorySchema", "DocumentSchema",
    "M_SCH", "O_SCH", "DIR_SCH", "DOC_SCH"
]


class ModelSchema(BaseModel):
    namespace: ClassVar[str]
    name: str
    primary_key: str
    attrs: list[A_SCH]

    def get_attr(self, name: str) -> A_SCH | None:
        for attr in self.attrs:
            if attr.name == name:
                return attr

    def get_columns(self) -> list[COL_SCH]:
        return list(filter(lambda a: a.attr == Attrs.COLUMN, self.attrs))

    def get_relations(self) -> list[REL_SCH]:
        return list(filter(lambda a: a.attr == Attrs.RELATION, self.attrs))

    def get_composites(self) -> list[COMP_SCH]:
        return list(filter(lambda a: a.attr == Attrs.COMPOSITE, self.attrs))

    def get_properties(self) -> list[PROP_SCH]:
        return list(filter(lambda a: a.attr == Attrs.PROPERTY, self.attrs))

    @property
    def full_name(self) -> str:
        return f'{self.namespace}.{self.name}'


class ObjectSchema(ModelSchema):
    def get_lists(self) -> list[LIST_SCH]:
        return list(filter(lambda a: a.attr == Attrs.LIST, self.attrs))


class DirectorySchema(ObjectSchema):
    namespace: ClassVar[str] = 'directories'


class DocumentSchema(ObjectSchema):
    namespace: ClassVar[str] = 'documents'
    prefix: str


M_SCH = TypeVar('M_SCH', bound=ModelSchema)
O_SCH = TypeVar('O_SCH', bound=ObjectSchema)
DIR_SCH = TypeVar('DIR_SCH', bound=DirectorySchema)
DOC_SCH = TypeVar('DOC_SCH', bound=DocumentSchema)
