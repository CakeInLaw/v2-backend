from datetime import date

from core.schemas.models.columns import DateSchema
from ._base import ColumnValidator
from ...exceptions import DateGteError, DateLteError


__all__ = ["DateValidator"]


class DateValidator(ColumnValidator[DateSchema, date]):
    python_type = date

    def _init_validators(self):
        if self._schema.gte is not None:
            self._validators.append(self._validate_gte)
        if self._schema.lte is not None:
            self._validators.append(self._validate_lte)

    def _transform(self, value: date | str) -> date:
        if isinstance(value, str):
            value = date.fromisoformat(value)
        return value

    def _validate_gte(self, value: date):
        if value < self._schema.gte:
            raise DateGteError(value=self._schema.gte)

    def _validate_lte(self, value: date):
        if value > self._schema.lte:
            raise DateLteError(value=self._schema.lte)
