from typing import TypeVar, ClassVar

from pydantic import BaseModel, computed_field

from .._types import Attrs


__all__ = ["AttrSchema", "A_SCH"]


class AttrSchema(BaseModel):
    name: str
    owner: str
    _attr: ClassVar[Attrs]

    @computed_field
    @property
    def attr(self) -> Attrs:
        return self._attr


A_SCH = TypeVar("A_SCH", bound=AttrSchema)
