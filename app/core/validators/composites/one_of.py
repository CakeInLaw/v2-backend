from typing import Any, Sequence

from core.schemas.models.composite import OneOfCompositeSchema

from ._base import CompositeValidator


__all__ = ["OneOfValidator"]


class OneOfValidator(CompositeValidator[OneOfCompositeSchema, tuple[str, Any]]):
    def transform(self, value: Sequence[str, Any]) -> dict[str, Any]:
        if not isinstance(value, Sequence) and not len(value) == 2:
            raise ValueError(f'tuple[col_name, col_value] expected, got {value}')
        col_name, col_value = value
        if col_name not in self._schema.attrs:
            raise ValueError(f'{col_name} not in {self._schema.attrs}')
        return {
            attr: col_value if attr == col_name else None
            for attr in self._schema.attrs
        }
