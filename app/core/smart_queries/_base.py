from typing import Any

from core.schema import O_SCH


class SmartQuery[T]:
    schema: O_SCH

    def get(
            self,
            filters: dict[str, Any] = None,
            sort: list[str] = None,
            include: dict[str, Any] = None,
    ):
        raise NotImplementedError

    @classmethod
    def get_pk_attr(cls) -> str:
        return cls.schema.primary_key

    def get_many(self, pks: list):
        return self.get(filters={self.get_pk_attr(): ('in', pks)})
