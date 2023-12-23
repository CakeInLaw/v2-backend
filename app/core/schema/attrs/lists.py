from typing import ClassVar, TypeVar

from ._base import AttrSchema, A_SCH
from .columns import COL_SCH
from .relations import REL_SCH
from .composites import COMP_SCH
from .properties import PROP_SCH
from .._types import Attrs


__all__ = ["ListSchema", "LIST_SCH"]


class ListSchema(AttrSchema):
    _attr: ClassVar[Attrs] = Attrs.LIST

    attrs: list[A_SCH]

    def get_columns(self) -> list[COL_SCH]:
        return list(filter(lambda a: a.type == Attrs.COLUMN, self.attrs))

    def get_relations(self) -> list[REL_SCH]:
        return list(filter(lambda a: a.type == Attrs.RELATION, self.attrs))

    def get_composites(self) -> list[COMP_SCH]:
        return list(filter(lambda a: a.type == Attrs.COMPOSITE, self.attrs))

    def get_properties(self) -> list[PROP_SCH]:
        return list(filter(lambda a: a.type == Attrs.PROPERTY, self.attrs))


LIST_SCH = TypeVar('LIST_SCH', bound=ListSchema)
