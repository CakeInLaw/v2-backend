from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped

from core.db.models import Directory
from core.db.hybrid import hybrid_property_helper
from core.db import types
from enums import UserRoles


class User(Directory):
    username: Mapped[str] = types.string(min_length=4, max_length=20, unique=True)

    password_hash: Mapped[str] = types.string(max_length=100, hidden=True)
    password_changed_at: Mapped[str] = types.datetime(timezone=True, hidden=True)

    role: Mapped[UserRoles] = types.enum(UserRoles)

    @hybrid_property_helper(
        required=True,
        readable=False,
        # обязательны 1 буква и цифра; допустимы буквы (латиница), цифры и !@#$%^&*-_=+
        setter_pattern='^(?=.*[A-Za-z])(?=.*[0-9])[A-Za-z0-9!@#$%^&*-_=+]{8,30}$',
        setter_min_length=8,
        setter_max_length=30,
    )
    @hybrid_property
    def password(self) -> str:
        return getattr(self, '_orig_password', None)

    @password.inplace.setter
    def _password_setter(self, value: str) -> None:
        setattr(self, '_orig_password', value)
