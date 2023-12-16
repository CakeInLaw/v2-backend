from typing import Generic, TypeVar, Callable, Literal, Self, overload, Optional, Any


__all__ = ["gen_property"]

T = TypeVar('T')


class GenProperty(Generic[T]):
    def __init__(self, getter: Callable[..., T], name: str = None):
        self.getter = getter
        self.name = name or self.getter.__name__

    @overload
    def __get__(self, instance: Literal[None], owner: Any) -> Self: ...

    @overload
    def __get__(self, instance: object, owner: Any) -> T: ...

    def __get__(self, instance: Optional[object], owner: Any) -> T | Self:
        if instance is None:
            return self
        return self.getter(instance)


@overload
def gen_property(getter_or_name: str) -> Callable[[Callable[..., T]], GenProperty[T]]: ...


@overload
def gen_property(getter_or_name: Callable[..., T]) -> GenProperty[T]: ...


def gen_property(getter_or_name):
    if isinstance(getter_or_name, str):
        return lambda getter: GenProperty(getter=getter, name=getter_or_name)
    else:
        return GenProperty(getter=getter_or_name)
