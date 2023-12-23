from typing import ClassVar, TypeVar

from ._base import AttrSchema, A_SCH
from .._types import Attrs


__all__ = ["ListSchema", "LIST_SCH"]


class ListSchema(AttrSchema):
    _attr: ClassVar[Attrs] = Attrs.LIST

    attrs: list[A_SCH]


LIST_SCH = TypeVar('LIST_SCH', bound=ListSchema)
