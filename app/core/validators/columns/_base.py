from typing import Generic, TypeVar, Callable, Type

from core.schemas.models.columns import ColumnSchema
from ..exceptions import NonNullable

CSH = TypeVar('CSH', bound=ColumnSchema)
T = TypeVar('T')


class ColumnValidator(Generic[CSH, T]):
    python_type: Type[T]

    def __init__(self, schema: CSH):
        self._schema = schema
        self._validators: list[Callable[[T], None]] = []
        self._init_validators()

    def _init_validators(self):
        pass

    def validate(self, value: T):
        if value is None:
            if not self._schema.nullable:
                raise NonNullable
            return
        for validator in self._validators:
            validator(value)

    def _transform(self, value: T) -> T:
        return value

    def transform(self, value: T) -> T:
        """
        Brings the value to the desired type before validation.
        Don`t override this method. Override "_transform" to specify all transform cases.
        """
        value = self._transform(value=value)
        assert isinstance(value, self.python_type), \
            f'Incorrect type. {self.python_type} expected, got {type(value)}; {value}'
        return value
