from asyncio import iscoroutinefunction
from inspect import getfullargspec
from typing import TypeVar, Type, Any, TYPE_CHECKING, final, Generic, Callable

from core.schemas.models.columns import C_SCH
from .._attrs import AttrValidator
from ...exceptions import NonNullable, NotUnique

if TYPE_CHECKING:
    from core.repositories import M_REP

__all__ = ["ColumnValidator", "COL_VAL"]

T = TypeVar('T')
COL_VAL = TypeVar('COL_VAL', bound="ColumnValidator")


class ColumnValidator(AttrValidator[C_SCH, T]):
    python_type: Type[T]

    def _post_init(self):
        self._validators: list[ColumnValidatorFunc] = []
        self._init_validators()
        if self.should_validate_unique():
            self.add_validator(self._validate_unique)

    def _init_validators(self):
        pass

    @final
    async def validate(self, value: T, repository: "M_REP") -> None:
        if value is None:
            if not self.schema.nullable:
                raise NonNullable
            return
        for validator in self._validators:
            await validator(value=value, repository=repository)

    def add_validator(self, func: Callable):
        self._validators.append(ColumnValidatorFunc(func))

    def _transform(self, value: Any) -> T:
        return value

    @final
    async def transform(self, value: Any, repository: "M_REP") -> T:
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
        return not (self.schema.hidden or self.schema.read_only)

    def is_required(self) -> bool:
        return not self.schema.has_default

    def modify_model_validator(self):
        if self.is_available():
            self.model_validator.available_attrs[self.schema.name] = self
            if self.is_required():
                self.model_validator.required_attrs.add(self.schema.name)

    def should_validate_unique(self):
        pks = self.model_validator.schema.primary_keys
        return self.schema.unique or (len(pks) == 1 and pks[0] == self.schema.name)

    async def _validate_unique(self, value: Any, repository: "M_REP"):
        if not await repository.check_unique(self.schema.name, value=value):
            raise NotUnique


class ColumnValidatorFunc(Generic[T]):
    as_is = False

    def __init__(self, func: Callable):
        self.func = func
        spec = getfullargspec(func)
        if spec.defaults:
            optional_args = spec.args[len(spec.args) - len(spec.defaults):]
            required_args = spec.args[:len(spec.args) - len(spec.defaults)]
        else:
            optional_args = []
            required_args = [*spec.args]
        if spec.kwonlydefaults:
            for key in spec.kwonlyargs:
                if key in spec.kwonlydefaults:
                    optional_args.append(key)
                else:
                    required_args.append(key)
        else:
            required_args.extend(spec.kwonlyargs)

        if 'self' in required_args:
            required_args.remove('self')
        available_args = self.get_available_args()
        assert all(arg in available_args for arg in required_args), \
            f'{required_args} not all in {available_args}'

        self.args = {*required_args, *optional_args}
        if spec.varkw:
            self.as_is = True
        self.coro = iscoroutinefunction(self.func)

    def filter_kwargs(self, **kwargs):
        if self.as_is:
            return kwargs
        return {k: v for k, v in kwargs.items() if k in self.args}

    async def __call__(self, value: T, repository: "M_REP"):
        kwargs = self.filter_kwargs(value=value, repository=repository)
        if self.coro:
            await self.func(**kwargs)
        else:
            self.func(**kwargs)

    @classmethod
    def get_available_args(cls):
        return getfullargspec(cls.__call__).args[1:]
