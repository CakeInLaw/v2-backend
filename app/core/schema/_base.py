from typing import TypeVar

from pydantic import BaseModel


__all__ = ["SCH"]

SCH = TypeVar('SCH', bound=BaseModel)
