from typing import ClassVar, TypeVar

from pydantic import InstanceOf

from ._base import AttrSchema
from .._types import Attrs


__all__ = ["ListSchema", "LIST_SCH"]


class ListSchema(AttrSchema):
    _attr_type: ClassVar[Attrs] = Attrs.LIST

    attrs: list[InstanceOf[AttrSchema]]


LIST_SCH = TypeVar('LIST_SCH', bound=ListSchema)
