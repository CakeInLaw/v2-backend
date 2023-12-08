from typing import Any, Sequence

from core.db.composite import OneOfComposite
from core.schemas.models.composite import OneOfCompositeSchema
from ._base import CompositeValidator
from ..exceptions import ValidationError, NonNullable


__all__ = ["OneOfValidator"]


class OneOfValidator(CompositeValidator[OneOfCompositeSchema, tuple[str, Any]]):
    async def validate(self, value: OneOfComposite):
        if value.__is_empty__():
            if not self._schema.nullable:
                raise NonNullable
            return
        try:
            await self._model_validator.get_attr(value.__current_set__).validate(value=value.__current_value__)
        except ValidationError as e:
            raise e(col_name=value.__current_set__)

    async def transform(self, value: tuple[str, Any]):
        if value is None:
            return self._schema.original_cls.__empty__()
        else:
            if not isinstance(value, Sequence) and not len(value) == 2:
                raise ValueError(f'tuple[col_name, col_value] expected, got {value}')
        if value[0] not in self._schema.attrs:
            raise ValueError(f'{value[0]} not in {self._schema.attrs}')
        return self._schema.original_cls.__from_kv__(*value)

    def modify_model_validator(self):
        if self._schema.required:
            self._model_validator.required_attrs.add(self._schema.name)
        for col_name in self._schema.attrs:
            self._model_validator.available_attrs.pop(col_name, None)
