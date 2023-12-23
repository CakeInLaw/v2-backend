from core.schemas.models.columns import BooleanSchema
from ._base import ColumnValidator


__all__ = ["BooleanValidator"]

BOOL_TRUE = {1, '1', 'on', 't', 'true', 'y', 'yes'}
BOOL_FALSE = {0, '0', 'off', 'f', 'false', 'n', 'no'}


class BooleanValidator(ColumnValidator[BooleanSchema, bool]):
    python_type = bool

    def _transform(self, value: str | int | bool) -> bool:
        if not (value is None or value is True or value is False):
            if value in BOOL_TRUE:
                value = True
            elif value in BOOL_FALSE:
                value = False
            else:
                raise ValueError(f'Impossible to bring {value} to bool')
        return value
