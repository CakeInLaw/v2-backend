from asyncio import iscoroutinefunction
from typing import Generic, TypeVar, Callable, Type, Coroutine, Any, TYPE_CHECKING

from core.schemas.models.columns import C_SCH
from ...exceptions import NonNullable

if TYPE_CHECKING:
    from core.repositories import M_REP
    from .._base import MV

__all__ = ["ColumnValidator", "CV"]

T = TypeVar('T')


class ColumnValidator(Generic[C_SCH, T]):
    python_type: Type[T]

    def __init__(self, schema: C_SCH, model_validator: Type["MV"]):
        self._schema = schema
        self._model_validator = model_validator

        self._validators: list[Callable[[T], None] | Callable[[T], Coroutine[Any, Any, None]]] = []
        self._init_validators()

    def _init_validators(self):
        pass

    async def validate(self, value: T, ):
        if value is None:
            if not self._schema.nullable:
                raise NonNullable
            return
        for validator in self._validators:
            if iscoroutinefunction(validator):
                await validator(value)
            else:
                validator(value)

    def _transform(self, value: T) -> T:
        return value

    async def transform(self, value: T, repository: M_REP) -> T:
        """
        Brings the value to the desired type before validation.
        Don`t override this method. Override "_transform" to specify all transform cases.
        """
        if iscoroutinefunction(self._transform):
            value = await self._transform(value=value)
        else:
            value = self._transform(value=value)
        assert isinstance(value, self.python_type), \
            f'Incorrect type. {self.python_type} expected, got {type(value)}; {value}'
        return value

    def is_available(self) -> bool:
        return not self._schema.read_only

    def is_required(self) -> bool:
        return not self._schema.read_only and self._schema.required


CV = TypeVar('CV', bound=ColumnValidator)
