from datetime import datetime

from core.schemas.models.columns import DateTimeSchema
from ._base import ColumnValidator
from ...exceptions import DateTimeGteError, DateTimeLteError, DateTimeTimezoneAwareError, DateTimeTimezoneNaiveError


__all__ = ["DateTimeValidator"]


class DateTimeValidator(ColumnValidator[DateTimeSchema, datetime]):
    python_type = datetime

    def _init_validators(self):
        if self.schema.gte is not None:
            self.add_validator(self._validate_gte)
        if self.schema.lte is not None:
            self.add_validator(self._validate_lte)
        if self.schema.with_timezone:
            self.add_validator(self._validate_aware)
        else:
            self.add_validator(self._validate_naive)

    def _transform(self, value: str | datetime) -> datetime:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value

    def _validate_gte(self, value: datetime):
        if value < self.schema.gte:
            raise DateTimeGteError(value=self.schema.gte)

    def _validate_lte(self, value: datetime):
        if value > self.schema.lte:
            raise DateTimeLteError(value=self.schema.lte)

    @staticmethod
    def _validate_naive(value: datetime):
        if value.tzinfo is not None:
            raise DateTimeTimezoneNaiveError

    @staticmethod
    def _validate_aware(value: datetime):
        if value.tzinfo is None:
            raise DateTimeTimezoneAwareError
