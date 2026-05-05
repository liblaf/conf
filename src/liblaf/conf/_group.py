"""Descriptors for lazily created nested configuration groups."""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from typing import Self, overload


@dataclasses.dataclass(frozen=True, slots=True, weakref_slot=True)
class Group[T]:
    """Descriptor that lazily attaches a nested object to a config instance.

    `BaseConfig` helpers such as `set()`, `load_env()`, and `to_dict()` expect
    group values to be nested [`BaseConfig`][liblaf.conf.BaseConfig] objects.
    The descriptor itself can cache any zero-argument factory result.
    """

    factory: Callable[[], T]
    name: str = dataclasses.field(init=False)

    @overload
    def __get__(self, instance: None, owner: type | None = None) -> Self: ...
    @overload
    def __get__(self, instance: object, owner: type | None = None) -> T: ...
    def __get__(self, instance: object | None, owner: type | None = None) -> Self | T:
        """Return this descriptor on classes or a cached group value on objects."""
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = self.factory()
        return instance.__dict__[self.name]

    def __set_name__(self, owner: type, name: str) -> None:
        """Record the group name assigned by the owning config class."""
        object.__setattr__(self, "name", name)


@overload
def group[T](factory: type[T]) -> Group[T]: ...
@overload
def group[T](factory: Callable[[], T]) -> Group[T]: ...
def group[T](factory: Callable[[], T]) -> Group[T]:
    """Create a [`Group`][liblaf.conf.Group] descriptor.

    Args:
        factory: A config class or zero-argument callable that creates the
            nested object.

    Returns:
        A group descriptor that caches one factory result per owning instance.
    """
    return Group(factory)
