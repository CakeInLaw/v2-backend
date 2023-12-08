from typing import TypeVar, Any, Generic, Type, cast

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Model, MODEL
from core.schemas import get_model_schema
from core.schemas.models import M_SCH

from core.validators.models import M_VAL, ModelValidator

__all__ = ["ModelRepository", "M_REP"]

_M = TypeVar('_M', bound=Model)


class ModelRepositoryMeta(type):
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        new_cls = cast(Type[MR], super().__new__(mcs, name, bases, attrs))
        if not hasattr(new_cls, 'model'):
            return new_cls
        new_cls.schema = get_model_schema(new_cls.model)
        new_cls.validator = new_cls.validator.bind(new_cls.schema)
        return new_cls


class ModelRepository(Generic[MODEL, M_VAL, M_SCH], metaclass=ModelRepositoryMeta):
    model: Type[MODEL]
    validator: Type[M_VAL] = ModelValidator
    schema: M_SCH

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_related(self, rel_name: str, pk: Any) -> _M:
        pass

    async def check_unique(self, attr_name: str, value: Any) -> bool:
        pass


M_REP = TypeVar('M_REP', bound=ModelRepository)
