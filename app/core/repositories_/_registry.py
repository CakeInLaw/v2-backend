from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from core.repositories import O_REP


__all__ = ["register_repository", "get_repository"]

registered_repositories: dict[tuple[str, str], Type["O_REP"]] = {}


def register_repository(repository_cls: Type["O_REP"], name: str = 'default'):
    registered_repositories[repository_cls.model.__full_name__, name] = repository_cls


def get_repository(model_full_name: str, repo_name: str = 'default') -> Type["O_REP"]:
    return registered_repositories[(model_full_name, repo_name)]
