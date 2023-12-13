from core.schemas.models.columns import IntegerSchema
from ._base import ColumnValidator
from ...exceptions import IntegerGteError, IntegerLteError


__all__ = ["IntegerValidator"]


class IntegerValidator(ColumnValidator[IntegerSchema, int]):
    python_type = int

    def _init_validators(self):
        if self.schema.gte is not None:
            self.add_validator(self._validate_gte)
        if self.schema.lte is not None:
            self.add_validator(self._validate_lte)

    def _transform(self, value: str | int) -> int:
        if isinstance(value, str):
            value = int(value)
        return value

    def _validate_gte(self, value: int):
        if value < self.schema.gte:
            raise IntegerGteError(value=self.schema.gte)

    def _validate_lte(self, value: int):
        if value > self.schema.lte:
            raise IntegerLteError(value=self.schema.lte)
