from datetime import datetime

from core.schemas.models.columns import DateTimeSchema
from ._base import ColumnValidator
from ...exceptions import DateTimeGteError, DateTimeLteError, DateTimeTimezoneAwareError, DateTimeTimezoneNaiveError


__all__ = ["DateTimeValidator"]


class DateTimeValidator(ColumnValidator[DateTimeSchema, datetime]):
    python_type = datetime

    def _init_validators(self):
        if self._schema.gte is not None:
            self._validators.append(self._validate_gte)
        if self._schema.lte is not None:
            self._validators.append(self._validate_lte)
        if self._schema.with_timezone:
            self._validators.append(self._validate_aware)
        else:
            self._validators.append(self._validate_naive)

    def _transform(self, value: datetime | str) -> datetime:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value

    def _validate_gte(self, value: datetime):
        if value < self._schema.gte:
            raise DateTimeGteError(value=self._schema.gte)

    def _validate_lte(self, value: datetime):
        if value > self._schema.lte:
            raise DateTimeLteError(value=self._schema.lte)

    @staticmethod
    def _validate_naive(value: datetime):
        if value.tzinfo is not None:
            raise DateTimeTimezoneNaiveError

    @staticmethod
    def _validate_aware(value: datetime):
        if value.tzinfo is None:
            raise DateTimeTimezoneAwareError
