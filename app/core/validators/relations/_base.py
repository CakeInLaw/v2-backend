from typing import TypeVar, Generic

from core.schemas.models.composite import CompositeSchema


CSH = TypeVar('CSH', bound=CompositeSchema)


class CompositeValidator(Generic[T]):
    def __init__(self, schema: CSH):
        self._schema = schema

    def validate(self, value: ):
        pass

    def transform(self, value: ):
