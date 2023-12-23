from typing import ClassVar, TypeVar

from pydantic import computed_field

from ._base import AttrSchema
from ._constraints import C
from .._types import Attrs, Types

__all__ = ["PropertySchema", "PROP_SCH"]


class PropertySchema(AttrSchema):
    _attr: ClassVar[Attrs] = Attrs.PROPERTY

    required: bool
    getter_constraints: C | None
    setter_constraints: C | None

    @computed_field
    @property
    def getter_type(self) -> Types | None:
        if self.getter_constraints is None:
            return
        return self.getter_constraints.type

    @computed_field
    @property
    def setter_type(self) -> Types | None:
        if self.setter_constraints is None:
            return
        return self.setter_constraints.type


PROP_SCH = TypeVar('PROP_SCH', bound=PropertySchema)
