from enum import IntEnum

__all__ = ["UserRoles"]


class UserRoles(IntEnum):
    SUPERUSER = 1
    CHIEF_COOK = 2
    TOVAROVED = 3
    COOK = 4
