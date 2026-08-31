"""Shared typing protocols and aliases used by config descriptors."""

from collections.abc import Callable
from typing import Any, ClassVar, Protocol


class ConfigProtocol(Protocol):
    """Minimum config interface required by [`Field`][liblaf.conf.Field]."""

    name: ClassVar[str]
    env_prefix: ClassVar[str]


type Converter[T] = Callable[[Any], T]
type Factory[T] = Callable[[], T]
