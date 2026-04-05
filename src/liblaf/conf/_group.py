"""Descriptors for lazily created nested configuration groups."""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from typing import Self, overload


@dataclasses.dataclass(frozen=True, slots=True, weakref_slot=True)
class Group[T]:
    """Cache a nested config or computed object per owning instance."""

    factory: Callable[[], T]
    name: str = dataclasses.field(init=False)

    @overload
    def __get__(self, instance: None, owner: type | None = None) -> Self: ...
    @overload
    def __get__(self, instance: object, owner: type | None = None) -> T: ...
    def __get__(self, instance: object | None, owner: type | None = None) -> Self | T:
        """Return the descriptor on the class or the cached group value."""
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = self.factory()
        return instance.__dict__[self.name]

    def __set_name__(self, owner: type, name: str) -> None:
        """Record the attribute name assigned by the owning class."""
        object.__setattr__(self, "name", name)


@overload
def group[T](factory: type[T]) -> Group[T]: ...
@overload
def group[T](factory: Callable[[], T]) -> Group[T]: ...
def group[T](factory: Callable[[], T]) -> Group[T]:
    """Wrap a config subclass or zero-argument callable as a group descriptor."""
    return Group(factory)
