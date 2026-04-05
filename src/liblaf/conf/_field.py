"""Field descriptors that bind config attributes to `Var` instances."""

import dataclasses
from typing import Self, overload

from . import converters
from ._sentinel import MISSING, MissingType
from ._types import ConfigProtocol, Converter, Factory
from ._var import Var


@dataclasses.dataclass(frozen=True, slots=True, weakref_slot=True)
class Field[T]:
    """Describe a config value and lazily bind it to a `Var`.

    The descriptor stores the environment-variable name, default value, optional
    factory, and string converter used when it creates a bound variable for a
    config instance.
    """

    env: str | None = None
    default: T | MissingType = MISSING
    factory: Factory[T] | None = None
    converter: Converter[T] = converters.identity
    name: str = dataclasses.field(init=False)

    @overload
    def __get__(self, instance: None, owner: type | None = None) -> Self: ...
    @overload
    def __get__(self, instance: object, owner: type | None = None) -> Var[T]: ...
    def __get__(
        self, instance: ConfigProtocol | None, owner: type | None = None
    ) -> Self | Var[T]:
        """Return the descriptor on the class or a cached bound variable."""
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = self._bind(instance)
        return instance.__dict__[self.name]

    def __set_name__(self, owner: type, name: str) -> None:
        """Record the attribute name assigned by the owning config class."""
        object.__setattr__(self, "name", name)

    def _bind(self, instance: ConfigProtocol) -> Var[T]:
        """Create the `Var` instance used by one config object."""
        name: str = instance.name + "." + self.name
        env: str = self.env or instance.env_prefix + self.name.upper()
        return Var(
            name,
            default=self.default,
            factory=self.factory,
            env=env,
            converter=self.converter,
        )


def field[T](
    *,
    env: str | None = None,
    default: T | MissingType = MISSING,
    factory: Factory[T] | None = None,
    converter: Converter[T] = converters.identity,
) -> Field[T]:
    """Create a `Field` descriptor for a config attribute."""
    return Field(env=env, default=default, factory=factory, converter=converter)
