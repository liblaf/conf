"""Context-local configuration variables with environment loading helpers."""

import contextlib
import contextvars
import copy
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
    _default: T | MissingType
    _factory: Factory[T] | None
    _var: contextvars.ContextVar[T | MissingType]

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
            converter: Callable used to normalize environment strings, direct
                assignments, defaults, and factory results. Defaults to
                [`identity`][liblaf.conf.converters.identity].
        """
        if converter is None:
            converter: Converter[T] = converters.identity
        var: contextvars.ContextVar[T | MissingType] = contextvars.ContextVar(
            name, default=MISSING
        )
        object.__setattr__(self, "_var", var)
        object.__setattr__(self, "env", env)
        object.__setattr__(self, "converter", converter)
        object.__setattr__(self, "_default", default)
        object.__setattr__(self, "_factory", factory)
        self.load_env()

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

        Examples:
            >>> value = Var("example", default=1)
            >>> value.get()
            1
        """
        value = self._var.get()
        if value is MISSING:
            value = self._new_default()
            if value is MISSING:
                if default is MISSING:
                    raise LookupError(self.name)
                return default
            self._var.set(value)
        return cast("T", value)

    def set(self, value: T) -> contextvars.Token[T]:
        """Set the active value.

        Args:
            value: New value for the active context. It is normalized by this
                variable's converter before storage.

        Returns:
            A [`contextvars.Token`][] that can restore the previous value with
            [`reset()`][liblaf.conf.Var.reset].
        """
        return cast("contextvars.Token[T]", self._var.set(self.converter(value)))

    def reset(self, token: contextvars.Token[T]) -> None:
        """Restore a value captured by [`set()`][liblaf.conf.Var.set].

        Args:
            token: Token returned by a previous `set()` call.
        """
        self._var.reset(cast("contextvars.Token[T | MissingType]", token))

    def load_env(self) -> None:
        """Reload the current context from the environment or declared default.

        When the variable is absent, this clears a previous environment or
        explicit value in the current context. The next read materializes a
        fresh declared default or factory result.
        """
        if self.env is None:
            return
        value: str | None = os.getenv(self.env)
        if value is None:
            self._var.set(MISSING)
            return
        self.set(cast("T", value))

    @contextlib.contextmanager
    def override(self, value: T) -> Generator[None]:
        """Temporarily set a value in the active context.

        Args:
            value: Temporary value to expose inside the context.

        Yields:
            `None` while the override is active. The previous value is restored
            when the context exits.

        Examples:
            >>> value = Var("example", default="base")
            >>> with value.override("temporary"):
            ...     value.get()
            'temporary'
            >>> value.get()
            'base'
        """
        token = self.set(value)
        try:
            yield
        finally:
            self.reset(token)

    def _new_default(self) -> T | MissingType:
        if self._factory is not None:
            return self.converter(self._factory())
        if self._default is MISSING:
            return MISSING
        return self.converter(copy.deepcopy(self._default))
