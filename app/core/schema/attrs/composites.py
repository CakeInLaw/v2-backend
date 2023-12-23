from typing import ClassVar, TypeVar

from pydantic import computed_field

from ._base import AttrSchema
from .._types import Attrs, Composites


__all__ = [
    "CompositeSchema", "COMP_SCH",
    "OneOfCompositeSchema"
]


class CompositeSchema(AttrSchema):
    _attr: ClassVar[Attrs] = Attrs.COMPOSITE
    _type: ClassVar[Composites]

    attrs: list[str]

    @computed_field
    @property
    def type(self) -> Composites:
        return self._type


COMP_SCH = TypeVar('COMP_SCH', bound=CompositeSchema)


class OneOfCompositeSchema(CompositeSchema):
    _type: ClassVar[Composites] = Composites.ONE_OF

    nullable: bool
