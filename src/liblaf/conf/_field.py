import dataclasses
from collections.abc import Callable
from typing import Protocol, Self, overload

from ._sentinel import MISSING, MissingType
from ._var import Var


class _ConfigProtocol(Protocol):
    name: str
    env_prefix: str


type Converter[T] = Callable[[str], T]
type Factory[T] = Callable[[], T]


@dataclasses.dataclass(frozen=True, slots=True, weakref_slot=True)
class Field[T]:
    env: str | None = None
    default: T | MissingType = MISSING
    factory: Factory[T] | None = None
    converter: Converter[T] | None = None
    name: str = dataclasses.field(init=False)

    @overload
    def __get__(self, instance: None, owner: type | None = None) -> Self: ...
    @overload
    def __get__(
        self, instance: _ConfigProtocol, owner: type | None = None
    ) -> Var[T]: ...
    def __get__(
        self, instance: _ConfigProtocol | None, owner: type | None = None
    ) -> Self | Var[T]:
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = self._bind(instance)
        return instance.__dict__[self.name]

    def __set_name__(self, owner: type, name: str) -> None:
        object.__setattr__(self, "name", name)

    def _bind(self, instance: _ConfigProtocol) -> Var[T]:
        name: str = instance.name + "." + self.name
        env: str = self.env or instance.env_prefix + self.name.upper()
        return Var(
            name,
            default=self.default,
            factory=self.factory,
            env=env,
            converter=self.converter,
        )
