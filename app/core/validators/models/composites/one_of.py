from typing import Any, Sequence, TYPE_CHECKING

from core.db.composite import OneOfComposite
from core.schemas.models.composite import OneOfCompositeSchema
from ._base import CompositeValidator
from ...exceptions import ValidationError, NonNullable

if TYPE_CHECKING:
    from core.repositories import M_REP

__all__ = ["OneOfValidator"]


class OneOfValidator(CompositeValidator[OneOfCompositeSchema, OneOfComposite]):
    async def validate(self, value: OneOfComposite, repository: "M_REP"):
        if value.__is_empty__():
            if not self.schema.nullable:
                raise NonNullable
            return
        try:
            await self.model_validator.get_attr(value.__current_set__).validate(value=value.__current_value__)
        except ValidationError as e:
            raise e(col_name=value.__current_set__)

    async def transform(self, value: tuple[str, Any], repository: "M_REP") -> OneOfComposite:
        if value is None:
            return self.schema.original_cls.__empty__()
        else:
            if not isinstance(value, Sequence) and not len(value) == 2:
                raise ValueError(f'tuple[col_name, col_value] expected, got {value}')
        if value[0] not in self.schema.attrs:
            raise ValueError(f'{value[0]} not in {self.schema.attrs}')
        return self.schema.original_cls.__from_kv__(*value)

    def modify_model_validator(self):
        if self.schema.required:
            self.model_validator.required_attrs.add(self.schema.name)
        for col_name in self.schema.attrs:
            self.model_validator.available_attrs.pop(col_name, None)
