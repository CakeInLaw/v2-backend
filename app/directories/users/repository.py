import re
from typing import Any

from passlib.context import CryptContext
from sqlalchemy import BinaryExpression, func

from core.db.models import OBJECT
from core.repositories import DirectoryRepository
from .models import User


__all__ = ["UserRepository"]


class UserRepository(DirectoryRepository[User]):
    model = User

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _check_unique_whereclause(self, attr_name: str, value: Any) -> BinaryExpression[bool]:
        if attr_name == 'username':
            return func.lower(User.username) == value.lower()  # type: ignore
        return super()._check_unique_whereclause(attr_name=attr_name, value=value)

    async def create(self, data: dict[str, Any]) -> User:
        user: User = await super().create(data=data)
        print(user.password)
        self.set_password(user, user.password)

    @classmethod
    def set_password(cls, user: User, password: str):
        user.password_hash = cls.pwd_context.hash(password)
        user.password_changed_at = datetime.now
