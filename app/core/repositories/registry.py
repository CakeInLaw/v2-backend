from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from ._base import O_REP


__all__ = ["register", "get_repository", "DEFAULT_REPOSITORY_KEY"]


_repositories: dict[tuple[str, str], Type["O_REP"]] = {}
DEFAULT_REPOSITORY_KEY = 'default'


def register(variant: str = DEFAULT_REPOSITORY_KEY):
    def wrapper(repository: Type["O_REP"]) -> Type["O_REP"]:
        comb = (repository.schema.name, variant)
        assert comb not in _repositories
        _repositories[comb] = repository
        return repository
    return wrapper


def get_repository(name: str, variant: str = DEFAULT_REPOSITORY_KEY, raise_if_none: bool = True) -> Type["O_REP"]:
    rep = _repositories.get((name, variant))
    if rep is None and raise_if_none:
        raise ValueError(f'Repository with name "{name}" and variant "{variant}" not registered."')
    return rep
