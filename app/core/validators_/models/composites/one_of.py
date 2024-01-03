from typing import Any, Sequence, TYPE_CHECKING

from core.schemas.models.composite import OneOfCompositeSchema
from ._base import CompositeValidator
from ...exceptions import ValidationError, NonNullable

if TYPE_CHECKING:
    from core.repositories import O_REP

__all__ = ["OneOfValidator"]


class OneOfValidator(CompositeValidator[OneOfCompositeSchema, tuple[str, Any]]):
    async def validate(self, value: tuple[str, Any], repository: "O_REP"):
        if value is None:
            if not self.schema.nullable:
                raise NonNullable
            return
        attr, value = value
        try:
            await self.model_validator.get_attr(attr).validate(value=value)
        except ValidationError as e:
            raise e(col_name=attr)

    async def transform(self, value: tuple[str, Any], repository: "O_REP") -> tuple[str, Any] | None:
        if value is None:
            return
        else:
            if not isinstance(value, Sequence) and not len(value) == 2:
                raise ValueError(f'tuple[col_name, col_value] expected, got {value}')
        if value[0] not in self.schema.attrs:
            raise ValueError(f'{value[0]} not in {self.schema.attrs}')
        return value

    def modify_model_validator(self):
        if self.schema.required:
            self.model_validator.required_attrs.add(self.schema.name)
        for col_name in self.schema.attrs:
            self.model_validator.available_attrs.pop(col_name, None)
