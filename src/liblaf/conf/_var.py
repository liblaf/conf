"""Context-local configuration variables with environment loading helpers."""

import contextlib
import contextvars
import dataclasses
import os
from collections.abc import Generator
from typing import Any, cast, overload

from . import converters
from ._sentinel import MISSING, MissingType
from ._types import Converter, Factory


@dataclasses.dataclass(init=False, frozen=True, slots=True, weakref_slot=True)
class Var[T]:
    """Context-local storage for one configuration value.

    A `Var` can be seeded from an environment variable, a default value, or a
    factory. The active value is stored in a [`contextvars.ContextVar`][], so
    temporary overrides follow normal context propagation rules.
    """

    env: str | None
    converter: Converter[T]
    _var: contextvars.ContextVar[T]

    def __init__(
        self,
        name: str,
        default: T | MissingType = MISSING,
        factory: Factory[T] | None = None,
        env: str | None = None,
        converter: Converter[T] | None = None,
    ) -> None:
        """Create a context-local config variable.

        Args:
            name: Name assigned to the underlying
                [`contextvars.ContextVar`][].
            default: Default value used when `env` is unset.
            factory: Zero-argument callable used to create a default when
                `default` is omitted.
            env: Environment-variable name to read during initialization and
                later `load_env()` calls.
            converter: Callable used to convert environment strings to Python
                values. Defaults to [`identity`][liblaf.conf.converters.identity].
        """
        if converter is None:
            converter: Converter[T] = converters.identity
        if env is not None:
            value: str | None = os.getenv(env)
            if value is not None:
                default: T = cast("T", converter(value))
        if default is MISSING and factory is not None:
            default: T = factory()
        if default is MISSING:
            var: contextvars.ContextVar[T] = contextvars.ContextVar(name)
        else:
            var: contextvars.ContextVar[T] = contextvars.ContextVar(
                name, default=default
            )
        object.__setattr__(self, "_var", var)
        object.__setattr__(self, "env", env)
        object.__setattr__(self, "converter", converter)

    def __hash__(self) -> int:
        """Return the hash of the wrapped context variable."""
        return hash(self._var)

    @property
    def name(self) -> str:
        """Name of the wrapped [`contextvars.ContextVar`][]."""
        return self._var.name

    @overload
    def get(self) -> T: ...
    @overload
    def get(self, default: T, /) -> T: ...
    @overload
    def get[D](self, default: D, /) -> D | T: ...
    def get(self, default: Any = MISSING) -> T:
        """Return the active value.

        Args:
            default: Optional fallback returned when the variable has no value.

        Returns:
            The active context value, or `default` when provided and no value is
            set.
        """
        if default is MISSING:
            return self._var.get()
        return self._var.get(default)

    def set(self, value: T) -> contextvars.Token[T]:
        """Set the active value.

        Args:
            value: New value for the active context.

        Returns:
            A [`contextvars.Token`][] that can restore the previous value with
            [`reset()`][liblaf.conf.Var.reset].
        """
        return self._var.set(value)

    def reset(self, token: contextvars.Token[T]) -> None:
        """Restore a value captured by [`set()`][liblaf.conf.Var.set].

        Args:
            token: Token returned by a previous `set()` call.
        """
        self._var.reset(token)

    def load_env(self) -> None:
        """Reload the active value from the configured environment variable."""
        if self.env is None:
            return
        value: str | None = os.getenv(self.env)
        if value is None:
            return
        if self.converter is None:
            self.set(cast("T", value))
        else:
            self.set(self.converter(value))

    @contextlib.contextmanager
    def override(self, value: T) -> Generator[None]:
        """Temporarily set a value in the active context.

        Args:
            value: Temporary value to expose inside the context.

        Yields:
            `None` while the override is active. The previous value is restored
            when the context exits.
        """
        token: contextvars.Token[T] = self._var.set(value)
        try:
            yield
        finally:
            self._var.reset(token)
