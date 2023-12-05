import re

from core.schemas.models.columns import StringSchema
from ._base import ColumnValidator, T
from ..exceptions import StringMinLengthError, StringMaxLengthError, StringPatternError


class StringValidator(ColumnValidator[StringSchema, str]):
    python_type = str

    def __init__(self, schema: StringSchema):
        super().__init__(schema=schema)
        self.pattern = re.compile(self._schema.pattern) if self._schema.pattern else None

    def _init_validators(self):
        if self._schema.min_length is not None:
            self._validators.append(self._validate_min_length)
        if self._schema.max_length is not None:
            self._validators.append(self._validate_max_length)
        if self._schema.pattern is not None:
            self._validators.append(self._validate_pattern)

    def _transform(self, value: str) -> str:
        if isinstance(value, str):
            value = value.strip()
        return value

    def _validate_min_length(self, value: str):
        if len(value) < self._schema.min_length:
            raise StringMinLengthError(self._schema.min_length)

    def _validate_max_length(self, value: str):
        if len(value) > self._schema.max_length:
            raise StringMaxLengthError(self._schema.max_length)

    def _validate_pattern(self, value: str):
        if not self.pattern.match(value):
            raise StringPatternError
