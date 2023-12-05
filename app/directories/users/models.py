from sqlalchemy.orm import Mapped

from core.db.models import Directory
from core.db import types


class User(Directory):
    username: Mapped[str] = types.string(min_length=4, max_length=20, unique=True)

    password_hash: Mapped[str] = types.string(max_length=200)
    password_salt: Mapped[str] = types.string(max_length=200)
    password_changed_at: Mapped[str] = types.datetime(timezone=True)

    is_superuser: Mapped[bool] = types.boolean(default=False)
