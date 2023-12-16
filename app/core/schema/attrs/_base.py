from typing import TypeVar, ClassVar

from pydantic import BaseModel, computed_field

from .._types import Attrs


__all__ = ["AttrSchema", "A_SCH"]


class AttrSchema(BaseModel):
    name: str
    owner: str
    _attr_type: ClassVar[Attrs]

    @computed_field
    @property
    def attr_type(self) -> Attrs:
        return self._attr_type


A_SCH = TypeVar("A_SCH", bound=AttrSchema)
