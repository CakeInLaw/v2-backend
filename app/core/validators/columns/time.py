from datetime import time

from core.schemas.models.columns import TimeSchema
from ._base import ColumnValidator
from ..exceptions import TimeGteError, TimeLteError


class TimeValidator(ColumnValidator[TimeSchema, time]):
    python_type = time

    def _init_validators(self):
        if self._schema.gte is not None:
            self._validators.append(self._validate_gte)
        if self._schema.lte is not None:
            self._validators.append(self._validate_lte)

    def _transform(self, value: time | str) -> time:
        if isinstance(value, str):
            value = time.fromisoformat(value)
        return value

    def _validate_gte(self, value: time):
        if value < self._schema.gte:
            raise TimeGteError(value=self._schema.gte)

    def _validate_lte(self, value: time):
        if value > self._schema.lte:
            raise TimeGteError(value=self._schema.lte)

