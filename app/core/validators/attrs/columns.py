import enum
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
from inspect import iscoroutinefunction, getfullargspec
from typing import TypeVar, Type, Any, final, Callable, Generic
from uuid import UUID

from core import utils
from core.schema import (
    COL_SCH, Types,
    BooleanSchema, DateSchema, DateTimeSchema,
    EnumSchema, GuidSchema, IntegerSchema,
    NumericSchema, StringSchema, TimeSchema,
)
from ._base import AttrValidator, ParentRepository, AttrValidatorParent
from ._constraints import (
    CONSTR_VAL,
    BooleanConstraintValidator, DateConstraintValidator, DateTimeConstraintValidator,
    EnumConstraintValidator, GuidConstraintValidator, IntegerConstraintValidator,
    NumericConstraintValidator, StringConstraintValidator, TimeConstraintValidator,
)
from ..exceptions import NonNullable, NotUnique

__all__ = [
    "ColumnValidator", "COL_VAL", "get_column_validator",
    "BooleanValidator", "DateValidator", "DateTimeValidator",
    "EnumValidator", "GuidValidator", "IntegerValidator",
    "NumericValidator", "StringValidator", "TimeValidator",
]


T = TypeVar('T', bound=Any)


class ColumnValidator(AttrValidator[COL_SCH, T], Generic[COL_SCH, T, CONSTR_VAL]):
    python_type: Type[T]
    _constr_validator_cls: Type[CONSTR_VAL]

    def _post_init(self):
        self._constr_validator: CONSTR_VAL = self._constr_validator_cls(constr=self.schema.constraints)
        self._validators: list[ColumnValidatorFunc] = []
        self._init_validators()
        if self.should_validate_unique():
            self.add_validator(self._validate_unique)

    def _init_validators(self):
        for validator in self._constr_validator.get_validators():
            self.add_validator(validator)

    @final
    async def validate(self, value: T, repository: ParentRepository) -> None:
        if value is None:
            if not self.schema.nullable:
                raise NonNullable
            return
        for validator in self._validators:
            await validator(value=value, repository=repository)

    def add_validator(self, func: Callable, index: int = -1):
        assert not self.has_validator(func)
        if index == -1:
            self._validators.append(ColumnValidatorFunc(func))
        else:
            self._validators.insert(index, ColumnValidatorFunc(func))

    def has_validator(self, func: Callable) -> bool:
        return any(v.func is func for v in self._validators)

    def rm_validator(self, func: Callable):
        rm = None
        for val in self._validators:
            if val.func is func:
                rm = val
        if rm is None:
            raise ValueError(f'{self} has no validator {func}')
        self._validators.remove(rm)

    def _transform(self, value: Any, repository: ParentRepository) -> T:
        return value

    @final
    async def transform(self, value: Any, repository: ParentRepository) -> T:
        if iscoroutinefunction(self._transform):
            value = await self._transform(value=value, repository=repository)
        else:
            value = self._transform(value=value, repository=repository)
        assert isinstance(value, self.python_type), \
            f'Incorrect type. {self.python_type} expected, got {type(value)}; {value}'
        return value

    def is_available(self) -> bool:
        return not (self.schema.hidden or self.schema.read_only)

    def is_required(self) -> bool:
        return not self.schema.has_default

    def modify_model_validator(self):
        if self.is_available():
            self.parent.available_attrs[self.schema.name] = self
            if self.is_required():
                self.parent.required_attrs.add(self.schema.name)

    def should_validate_unique(self):
        if self._parent_is_list:
            return False
        pks = self.parent.schema.primary_keys
        return self.schema.unique or (len(pks) == 1 and pks[0] == self.schema.name)

    async def _validate_unique(self, value: Any, repository: ParentRepository):
        if not await repository.check_unique(self.schema.name, value=value):
            raise NotUnique


COL_VAL = TypeVar('COL_VAL', bound=ColumnValidator)


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

    async def __call__(self, value: T, repository: ParentRepository):
        kwargs = self.filter_kwargs(value=value, repository=repository)
        if self.coro:
            await self.func(**kwargs)
        else:
            self.func(**kwargs)

    @classmethod
    def get_available_args(cls):
        return getfullargspec(cls.__call__).args[1:]


class BooleanValidator(ColumnValidator[BooleanSchema, bool, BooleanConstraintValidator]):
    python_type = bool
    _constr_validator_cls = BooleanConstraintValidator

    BOOL_TRUE = {1, '1', 'on', 't', 'true', 'y', 'yes'}
    BOOL_FALSE = {0, '0', 'off', 'f', 'false', 'n', 'no'}

    def _transform(self, value: str | int | bool, repository: ParentRepository) -> bool:
        if not (value is None or value is True or value is False):
            if value in self.BOOL_TRUE:
                value = True
            elif value in self.BOOL_FALSE:
                value = False
            else:
                raise ValueError(f'Impossible to bring {value} to bool')
        return value


class DateValidator(ColumnValidator[DateSchema, date, DateConstraintValidator]):
    python_type = date
    _constr_validator_cls = DateConstraintValidator

    def _transform(self, value: str | date, repository: ParentRepository) -> date:
        if isinstance(value, str):
            value = date.fromisoformat(value)
        return value


class DateTimeValidator(ColumnValidator[DateTimeSchema, datetime, DateTimeConstraintValidator]):
    python_type = datetime
    _constr_validator_cls = DateTimeConstraintValidator

    def _transform(self, value: str | datetime, repository: ParentRepository) -> datetime:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value


ENUM = TypeVar('ENUM', enum.IntEnum, enum.StrEnum)


class EnumValidator(ColumnValidator[EnumSchema, ENUM, EnumConstraintValidator]):
    _constr_validator_cls = EnumConstraintValidator

    def _post_init(self):
        self.python_type = utils.import_string(f'enums.{self.schema.constraints.enum_type_name}')
        self.is_int_enum = issubclass(self.python_type, enum.IntEnum)
        self.is_str_enum = issubclass(self.python_type, enum.StrEnum)
        super()._post_init()

    def _transform(self, value: str | int | ENUM, repository: ParentRepository) -> ENUM:
        if isinstance(value, str):
            if self.is_int_enum:
                value = int(value)
            value = self.python_type(value)
        elif isinstance(value, int):
            if self.is_str_enum:
                value = str(value)
            value = self.python_type(value)
        return value


class GuidValidator(ColumnValidator[GuidSchema, UUID, GuidConstraintValidator]):
    python_type = UUID
    _constr_validator_cls = GuidConstraintValidator

    def _transform(self, value: str | UUID, repository: ParentRepository) -> UUID:
        if isinstance(value, str):
            value = UUID(value)
        return value


class IntegerValidator(ColumnValidator[IntegerSchema, int, IntegerConstraintValidator]):
    python_type = int
    _constr_validator_cls = IntegerConstraintValidator

    def _transform(self, value: str | int, repository: ParentRepository) -> int:
        if isinstance(value, str):
            value = int(value)
        return value


class NumericValidator(ColumnValidator[NumericSchema, Decimal, NumericConstraintValidator]):
    python_type = Decimal
    _constr_validator_cls = NumericConstraintValidator

    def _transform(self, value: str | int | float | Decimal, repository: ParentRepository) -> Decimal:
        if isinstance(value, (str, int, float)):
            try:
                value = Decimal(value)
            except InvalidOperation:
                raise ValueError(f'Incorrect decimal value, {value}')
        if isinstance(value, Decimal):
            return self.normalize(value)

    def normalize(self, value: Decimal):
        return value.quantize(self.step)

    @property
    def step(self) -> Decimal:
        return Decimal(f'0.{"0" * (self.schema.constraints.scale - 1)}1')


class StringValidator(ColumnValidator[StringSchema, str, StringConstraintValidator]):
    python_type = str
    _allowed_transform_types = (int, float)
    _constr_validator_cls = StringConstraintValidator

    def _transform(self, value: str, repository: ParentRepository) -> str:
        if not isinstance(value, str):
            if isinstance(value, self._allowed_transform_types):
                value = str(value)
            else:
                raise ValueError(f'Can`t convert {value} to str. Available types are {self._allowed_transform_types}')
        return value.strip()


class TimeValidator(ColumnValidator[TimeSchema, time, TimeConstraintValidator]):
    python_type = time
    _constr_validator_cls = TimeConstraintValidator

    def _transform(self, value: time | str, repository: ParentRepository) -> time:
        if isinstance(value, str):
            value = time.fromisoformat(value)
        return value


column_validators_map: dict[Types, Type[COL_VAL]] = {
    Types.BOOLEAN: BooleanValidator,
    Types.DATE: DateValidator,
    Types.DATETIME: DateTimeValidator,
    Types.ENUM: EnumValidator,
    Types.GUID: GuidValidator,
    Types.INTEGER: IntegerValidator,
    Types.NUMERIC: NumericValidator,
    Types.STRING: StringValidator,
    Types.TEXT: StringValidator,
    Types.TIME: TimeValidator,
}


def get_column_validator(schema: COL_SCH, parent: AttrValidatorParent) -> COL_VAL:
    return column_validators_map[schema.type](schema, parent=parent)
