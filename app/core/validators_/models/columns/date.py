from datetime import date

from core.schemas.models.columns import DateSchema
from ._base import ColumnValidator
from ...exceptions import DateGteError, DateLteError


__all__ = ["DateValidator"]


class DateValidator(ColumnValidator[DateSchema, date]):
    python_type = date

    def _init_validators(self):
        if self.schema.gte is not None:
            self.add_validator(self._validate_gte)
        if self.schema.lte is not None:
            self.add_validator(self._validate_lte)

    def _transform(self, value: str | date) -> date:
        if isinstance(value, str):
            value = date.fromisoformat(value)
        return value

    def _validate_gte(self, value: date):
        if value < self.schema.gte:
            raise DateGteError(value=self.schema.gte)

    def _validate_lte(self, value: date):
        if value > self.schema.lte:
            raise DateLteError(value=self.schema.lte)
