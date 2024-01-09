from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped

from core.db.models import Directory
from core.db.relations import one_to_one
from core.db import types

if TYPE_CHECKING:
    from directories.users.models import User


__all__ = ["Employee"]


class Employee(Directory):
    user_id, user = one_to_one('directories.users.id', nullable=True)
    user_id: Mapped[UUID]
    user: Mapped["User"]

    name: Mapped[str] = types.string(max_length=100)
