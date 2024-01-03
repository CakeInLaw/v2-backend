from inspect import getfullargspec, iscoroutinefunction
from typing import Generic, TypeVar, Any, TYPE_CHECKING, Type, Union, Callable

from core.schema import A_SCH
from ..exceptions import ValidationError, NonNullable, ListErrors

if TYPE_CHECKING:
    from core.repositories import O_REP, LIST_REP
    from ..models import M_VAL
    from .lists import LIST_VAL


__all__ = ["AttrValidator", "A_VAL", "AttrValidatorParent", "ParentRepository"]

T = TypeVar('T', bound=Any)
AttrValidatorParent = Type["M_VAL"] | Type["LIST_VAL"]
ParentRepository = Union["M_REP", "LIST_REP"]


class AttrValidator(Generic[A_SCH, T]):
    def __init__(self, schema: A_SCH, parent: AttrValidatorParent):
        self.schema = schema
        self.parent = parent
        self._validators: list[ValidatorFuncWrapper] = []
        self._post_init()

    def _post_init(self):
        pass

    async def validate(self, value: Any, repository: ParentRepository) -> T:
        raise NotImplementedError()

    async def validate_list(self, list_of_values: list, repository: ParentRepository) -> list[T]:  # TODO
        errors = ListErrors()
        for idx, value in enumerate(list_of_values):
            try:
                await self.validate(value=value, repository=repository)
            except ValidationError as err:
                errors.add(idx=idx, err=err)
        if errors:
            raise errors

    def modify_parent(self):
        pass

    def add_validator(self, func: Callable, index: int = -1):
        assert not self.has_validator(func)
        if index == -1:
            self._validators.append(ValidatorFuncWrapper(self, func))
        else:
            self._validators.insert(index, ValidatorFuncWrapper(self, func))

    def has_validator(self, func: Callable) -> bool:
        return any(val == func for val in self._validators)

    def rm_validator(self, func: Callable):
        rm = None
        for val in self._validators:
            if val == func:
                rm = val
        if rm is None:
            raise ValueError(f'{self} has no validator {func}')
        self._validators.remove(rm)

    def raise_if_non_nullable(self) -> None:
        if not self.schema.nullable:
            raise NonNullable


A_VAL = TypeVar('A_VAL', bound=AttrValidator)


class ValidatorFuncWrapper(Generic[T]):
    as_is = False

    def __init__(self, attr_validator: A_VAL, func: Callable):
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

        available_args = self.get_available_args(attr_validator)
        assert all(arg in available_args for arg in required_args), \
            f'{required_args} are not all in {available_args}'

        self.args = {*required_args, *optional_args}
        if spec.varkw:
            self.as_is = True
        self.coro = iscoroutinefunction(self.func)

    def filter_kwargs(self, kwargs):
        if self.as_is:
            return kwargs
        return {k: v for k, v in kwargs.items() if k in self.args}

    async def __call__(self, **kwargs):
        kwargs = self.filter_kwargs(kwargs)
        if self.coro:
            await self.func(**kwargs)
        else:
            self.func(**kwargs)

    @classmethod
    def get_available_args(cls, attr_validator: A_VAL):
        spec = getfullargspec(attr_validator.validate)
        return [arg != 'self' for arg in spec.args + spec.kwonlyargs]

    def __eq__(self, other):
        return self.func is other
