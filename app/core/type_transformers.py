from datetime import date, datetime, time, timezone
from decimal import Decimal, InvalidOperation
from typing import Type, Optional
from uuid import UUID

from core.types import ENUM


__all__ = [
    "transform_bool",
    "transform_date",
    "transform_datetime",
    "transform_enum",
    "transform_guid",
    "transform_integer",
    "transform_numeric",
    "transform_string",
    "transform_time",
]


BOOL_TRUE = {1, '1', 'on', 't', 'true', 'y', 'yes'}
BOOL_FALSE = {0, '0', 'off', 'f', 'false', 'n', 'no'}


def transform_bool(value: int | str | bool | None) -> bool | None:
    if not (value is True or value is False or value is None):
        if value in BOOL_TRUE:
            value = True
        elif value in BOOL_FALSE:
            value = False
        else:
            raise ValueError(f'Impossible to bring "{value}" to bool')
    return value


def transform_date(value: str | date | None) -> date | None:
    if value is None:
        return value
    if isinstance(value, str):
        value = date.fromisoformat(value)
    if not isinstance(value, date):
        raise ValueError(f'Impossible to bring "{value}" to date')
    return value


def transform_datetime(value: str | datetime | None, with_timezone: bool) -> datetime | None:
    if value is None:
        return value
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    if not isinstance(value, datetime):
        raise ValueError(f'Impossible to bring "{value}" to datetime')
    if with_timezone and value.tzinfo is None:
        value.replace(tzinfo=timezone.utc)
    if not with_timezone and value.tzinfo:
        value.astimezone(timezone.utc).replace(tzinfo=None)
    return value


def transform_enum(value: int | str | ENUM | None, python_enum: Type[ENUM]) -> Optional[ENUM]:
    if value is None:
        return
    if isinstance(value, python_enum):
        return value
    try:
        value = python_enum(value)
    except ValueError:
        raise ValueError(f'Impossible to bring "{value}" to {python_enum.__name__}')
    return value


def transform_guid(value: str | UUID | None) -> UUID | None:
    if value is None:
        return
    if isinstance(value, str):
        value = UUID(value)
    if not isinstance(value, UUID):
        raise ValueError(f'Impossible to bring "{value}" to UUID')
    return value


def transform_integer(value: int | str | None) -> int | None:
    if value is None:
        return
    if isinstance(value, str):
        value = int(value)
    if not isinstance(value, int):
        raise ValueError(f'Impossible to bring "{value}" to integer')
    return value


def transform_numeric(value: int | str | Decimal | None, precision: int, scale: int) -> Decimal | None:
    if value is None:
        return
    if isinstance(value, (str, int, float)):
        try:
            value = Decimal(value)
        except InvalidOperation:
            raise ValueError(f'Incorrect decimal value, {value}')
    if not isinstance(value, Decimal):
        raise ValueError(f'Impossible to bring "{value}" to Decimal')
    if -value.as_tuple().exponent != scale:
        step = Decimal(f'0.{"0" * (scale - 1)}1')
        value = value.quantize(step)
    if len(value.as_tuple().digits) > precision:
        raise ValueError(f'Value is too long. Max precision is {precision}')
    return value


_string_allowed_transform_types = (int, float, Decimal)


def transform_string(value: int | float | Decimal | str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        if isinstance(value, _string_allowed_transform_types):
            value = str(value)
        else:
            raise ValueError(f'Can`t convert "{value}" to str. Available types are {_string_allowed_transform_types}')
    return value.strip()


def transform_time(value: str | time | None) -> time | None:
    if value is None:
        return value
    if isinstance(value, str):
        value = time.fromisoformat(value)
    if not isinstance(value, time):
        raise ValueError(f'Impossible to bring "{value}" to date')
    return value
