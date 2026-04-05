"""Configuration containers built from fields and nested groups."""

from __future__ import annotations

import contextlib
import types
from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Self, cast

from pydantic import alias_generators

from ._field import Field
from ._group import Group

if TYPE_CHECKING:
    from ._var import Var


class ConfigMeta(type):
    """Build config classes and cache a singleton instance per subclass."""

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **_kwargs: Any,
    ) -> type:
        """Create a config class with derived metadata and descriptor maps."""
        if "name" not in namespace:
            namespace["name"] = alias_generators.to_snake(name).removesuffix("_config")
        if "env_prefix" not in namespace:
            namespace["env_prefix"] = namespace["name"].upper() + "_"
        cls: type[BaseConfig] = cast(
            "type[BaseConfig]", super().__new__(mcs, name, bases, namespace)
        )
        fields: dict[str, Field[Any]] = {}
        groups: dict[str, Group[Any]] = {}
        for base in reversed(cls.__mro__[1:]):
            fields.update(getattr(base, "_fields", {}))
            groups.update(getattr(base, "_groups", {}))
        for key, value in namespace.items():
            match value:
                case Field():
                    groups.pop(key, None)
                    fields[key] = value
                case Group():
                    fields.pop(key, None)
                    groups[key] = value
                case _:
                    fields.pop(key, None)
                    groups.pop(key, None)
        cls._fields = fields
        cls._groups = groups
        return cls

    def __call__[T: BaseConfig](cls: type[T], *args, **kwargs) -> T:
        """Return the cached config instance, creating it on first access."""
        instance: T | None = cls.__dict__.get("_instance")
        if instance is None:
            instance = super().__call__(*args, **kwargs)  # ty:ignore[invalid-super-argument]
            cls._instance = instance
        return instance


class BaseConfig(metaclass=ConfigMeta):
    """Group related configuration variables behind a singleton object.

    Subclasses declare [`Field`][liblaf.conf.Field] descriptors for scalar values
    and [`group`][liblaf.conf.group] descriptors for nested configuration
    sections. Instances expose helpers for loading environment variables,
    applying temporary overrides, and serializing the current state.
    """

    name: ClassVar[str]
    env_prefix: ClassVar[str]
    _fields: ClassVar[dict[str, Field[Any]]]
    _groups: ClassVar[dict[str, Group[Any]]]
    _instance: ClassVar[Self | None] = None

    def load_env(self) -> None:
        """Refresh every field from its configured environment variable."""
        for name in self._fields:
            var: Var[Any] = self._get_field(name)
            var.load_env()
        for name in self._groups:
            group: BaseConfig = self._get_group(name)
            group.load_env()

    def set(self, changes: Mapping[str, Any] | None = None, /, **kwargs: Any) -> None:
        """Update fields or groups from a mapping and keyword arguments.

        Nested groups accept mapping values and forward them to the nested
        config's own `set()` method.
        """
        if changes is not None:
            kwargs.update(changes)
        for name, value in kwargs.items():
            var: BaseConfig | Var[Any] = self._get_field_or_group(name)
            var.set(value)

    @contextlib.contextmanager
    def override(
        self, changes: Mapping[str, Any] | None = None, /, **kwargs: Any
    ) -> Generator[None]:
        """Temporarily override one or more values within a context manager.

        Args:
            changes: Optional mapping of names to temporary values.
            **kwargs: Additional name-to-value overrides.

        Yields:
            `None` while the overrides are active.
        """
        if changes is not None:
            kwargs.update(changes)
        with contextlib.ExitStack() as stack:
            for name, value in kwargs.items():
                var: BaseConfig | Var[Any] = self._get_field_or_group(name)
                stack.enter_context(var.override(value))
            yield

    def to_dict(self) -> dict[str, Any]:
        """Serialize the current config tree to nested dictionaries."""
        result: dict[str, Any] = {}
        for name in self._fields:
            result[name] = self._get_field(name).get()
        for name in self._groups:
            result[name] = self._get_group(name).to_dict()
        return result

    def to_namespace(self) -> types.SimpleNamespace:
        """Serialize the current config tree to nested namespaces."""
        result: types.SimpleNamespace = types.SimpleNamespace()
        for name in self._fields:
            setattr(result, name, self._get_field(name).get())
        for name in self._groups:
            setattr(result, name, self._get_group(name).to_namespace())
        return result

    def _get_field(self, name: str) -> Var[Any]:
        """Return the bound variable for a declared field name."""
        return getattr(self, name)

    def _get_field_or_group(self, name: str) -> BaseConfig | Var[Any]:
        """Return either a bound variable or nested config by name."""
        return getattr(self, name)

    def _get_group(self, name: str) -> BaseConfig:
        """Return the nested config instance for a declared group name."""
        return getattr(self, name)
