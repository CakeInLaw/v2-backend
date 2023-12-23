from typing import Generic, TypeVar, Callable, Literal, Self, overload, Optional, Any, Type

__all__ = ["gen_property"]

T = TypeVar('T', bound=Any)


class gen_property(Generic[T]):
    def __init__(self, getter: Callable[..., T]):
        self.getter = getter
        self.name = self.getter.__name__

    @overload
    def __get__(self, instance: Literal[None], owner: Optional[Type[object]]) -> Self: ...

    @overload
    def __get__(self, instance: object, owner: Optional[Type[object]]) -> T: ...

    def __get__(self, instance: Optional[object], owner: Optional[Type[object]]) -> T | Self:
        if instance is None:
            return self
        return self.getter(instance)
