from collections.abc import Callable
from typing import ClassVar, Protocol


class ConfigProtocol(Protocol):
    name: ClassVar[str]
    env_prefix: ClassVar[str]


type Converter[T] = Callable[[str], T]
type Factory[T] = Callable[[], T]
