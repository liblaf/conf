"""Field descriptors that bind config attributes to `Var` instances."""

import dataclasses
from typing import Self, overload

from . import converters
from ._sentinel import MISSING, MissingType
from ._types import ConfigProtocol, Converter, Factory
from ._var import Var


@dataclasses.dataclass(frozen=True, slots=True, weakref_slot=True)
class Field[T]:
    """Descriptor that declares one configuration value.

    A `Field` stores the environment-variable name, default or factory, and
    converter used to create a bound [`Var`][liblaf.conf.Var]. Binding is lazy:
    the `Var` is created the first time the field is accessed on a config
    instance.
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
        """Return this descriptor on classes or a cached bound `Var` on objects."""
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = self._bind(instance)
        return instance.__dict__[self.name]

    def __set_name__(self, owner: type, name: str) -> None:
        """Record the field name assigned by the owning config class."""
        object.__setattr__(self, "name", name)

    def _bind(self, instance: ConfigProtocol) -> Var[T]:
        """Create the `Var` used by one config instance."""
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
    """Create a [`Field`][liblaf.conf.Field] descriptor.

    Args:
        env: Explicit environment-variable name. When omitted, the owning
            config's `env_prefix` and the field name are combined.
        default: Default value used when no environment value is present.
        factory: Zero-argument callable used to create a default when `default`
            is omitted.
        converter: Callable used to normalize environment strings and direct
            Python assignments to the field value.

    Returns:
        A field descriptor ready to assign on a
        [`BaseConfig`][liblaf.conf.BaseConfig] subclass.
    """
    return Field(env=env, default=default, factory=factory, converter=converter)
