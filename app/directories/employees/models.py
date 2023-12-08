from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, relationship

from core.db.models import Directory
from core.db.relations import one_to_one
from core.db import types

if TYPE_CHECKING:
    from directories.users.models import User


class Employee(Directory):
    user_id: Mapped[UUID] = one_to_one('directories.users.id', nullable=True)
    user: Mapped["User"] = relationship(foreign_keys=[user_id])

    name: Mapped[str] = types.string(max_length=100)
