from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from .models import Employee


class EmployeeRepository[M: Employee]:
    model: M = Employee

    def __init__(self, session: AsyncSession, instance: M = None):
        self.session = session
        self.instance = instance

    def bind(self, instance: M):
        self.instance = instance

    def create(self, data: dict[str, Any]):
        self.session.add(self.model(**data))
