"""Shared typing protocols and aliases for the configuration package."""

from collections.abc import Callable
from typing import ClassVar, Protocol


class ConfigProtocol(Protocol):
    """Minimal protocol implemented by config instances bound to a `Field`."""

    name: ClassVar[str]
    env_prefix: ClassVar[str]


type Converter[T] = Callable[[str], T]
type Factory[T] = Callable[[], T]
