import re

from core.schemas.models.columns import StringSchema
from ._base import ColumnValidator
from ...exceptions import StringMinLengthError, StringMaxLengthError, StringPatternError


__all__ = ["StringValidator"]


class StringValidator(ColumnValidator[StringSchema, str]):
    python_type = str
    _allowed_transform_types = int, float

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pattern = re.compile(self.schema.pattern) if self.schema.pattern else None

    def _init_validators(self):
        if self.schema.min_length is not None:
            self.add_validator(self._validate_min_length)
        if self.schema.max_length is not None:
            self.add_validator(self._validate_max_length)
        if self.schema.pattern is not None:
            self.add_validator(self._validate_pattern)

    def _transform(self, value: str) -> str:
        if not isinstance(value, str):
            if isinstance(value, self._allowed_transform_types):
                value = str(value)
            else:
                raise ValueError(f'Can`t convert {value} to str. Available types are {self._allowed_transform_types}')
        return value.strip()

    def _validate_min_length(self, value: str):
        if len(value) < self.schema.min_length:
            raise StringMinLengthError(self.schema.min_length)

    def _validate_max_length(self, value: str):
        if len(value) > self.schema.max_length:
            raise StringMaxLengthError(self.schema.max_length)

    def _validate_pattern(self, value: str):
        if not self.pattern.match(value):
            raise StringPatternError
