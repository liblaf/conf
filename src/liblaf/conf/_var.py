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
        return hash(self._var)

    @property
    def name(self) -> str:
        return self._var.name

    @overload
    def get(self) -> T: ...
    @overload
    def get(self, default: T, /) -> T: ...
    @overload
    def get[D](self, default: D, /) -> D | T: ...
    def get(self, default: Any = MISSING) -> T:
        if default is MISSING:
            return self._var.get()
        return self._var.get(default)

    def set(self, value: T) -> contextvars.Token[T]:
        return self._var.set(value)

    def reset(self, token: contextvars.Token[T]) -> None:
        self._var.reset(token)

    def load_env(self) -> None:
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
        token: contextvars.Token[T] = self._var.set(value)
        try:
            yield
        finally:
            self._var.reset(token)
