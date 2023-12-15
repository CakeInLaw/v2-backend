from core.repositories import DirectoryRepository
from .models import Employee


__all__ = ["EmployeeRepository"]


class EmployeeRepository(DirectoryRepository[Employee]):
    model = Employee
