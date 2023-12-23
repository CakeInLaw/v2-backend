from datetime import time

from core.schemas.models.columns import TimeSchema
from ._base import ColumnValidator
from ...exceptions import TimeGteError, TimeLteError


__all__ = ["TimeValidator"]


class TimeValidator(ColumnValidator[TimeSchema, time]):
    python_type = time

    def _init_validators(self):
        if self.schema.gte is not None:
            self.add_validator(self._validate_gte)
        if self.schema.lte is not None:
            self.add_validator(self._validate_lte)

    def _transform(self, value: time | str) -> time:
        if isinstance(value, str):
            value = time.fromisoformat(value)
        return value

    def _validate_gte(self, value: time):
        if value < self.schema.gte:
            raise TimeGteError(value=self.schema.gte)

    def _validate_lte(self, value: time):
        if value > self.schema.lte:
            raise TimeLteError(value=self.schema.lte)
