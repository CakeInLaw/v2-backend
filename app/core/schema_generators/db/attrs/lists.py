from typing import Type

from sqlalchemy.orm import RelationshipProperty

from core.db.models import Model, ListModel
from core.schema.attrs import LIST_SCH
from ._base import AttrSchemaGenerator


class ListSchemaGenerator(AttrSchemaGenerator[LIST_SCH, RelationshipProperty]):

    @property
    def list(self) -> Type[ListModel]:
        if not hasattr(self, '_list_model_cached'):
            model = Model.find_by_table(self._attr.target)
            assert issubclass(model, ListModel)
            setattr(self, '_list_model_cached', model)
        return getattr(self, '_list_model_cached')
