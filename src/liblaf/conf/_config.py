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
    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **_kwargs: Any,
    ) -> type:
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
        for attr_name, attr_value in namespace.items():
            match attr_value:
                case Field():
                    fields[attr_name] = attr_value
                case Group():
                    groups[attr_name] = attr_value
        cls._fields = fields
        cls._groups = groups
        return cls

    def __call__[T: BaseConfig](cls: type[T], *args, **kwargs) -> T:
        if not getattr(cls, "singleton", True):
            return super().__call__(*args, **kwargs)  # ty:ignore[invalid-super-argument]
        if "_instance" not in cls.__dict__:
            cls.__dict__["_instance"] = super().__call__(*args, **kwargs)  # ty:ignore[invalid-super-argument]
        return cls.__dict__["_instance"]


class BaseConfig(metaclass=ConfigMeta):
    name: ClassVar[str]
    env_prefix: ClassVar[str]
    singleton: ClassVar[bool] = True
    _fields: ClassVar[dict[str, Field[Any]]]
    _groups: ClassVar[dict[str, Group[Any]]]
    _instance: ClassVar[Self | None] = None

    def set(self, changes: Mapping[str, Any] | None = None, /, **kwargs: Any) -> None:
        if changes is not None:
            kwargs.update(changes)
        for name, value in kwargs.items():
            var: BaseConfig | Var[Any] = self._get_field(name)
            var.set(value)

    @contextlib.contextmanager
    def override(
        self, changes: Mapping[str, Any] | None = None, /, **kwargs: Any
    ) -> Generator[None]:
        if changes is not None:
            kwargs.update(changes)
        with contextlib.ExitStack() as stack:
            for name, value in kwargs.items():
                var: BaseConfig | Var[Any] = self._get_field(name)
                stack.enter_context(var.override(value))
            yield

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for name in self._fields:
            result[name] = self._get_field(name).get()
        for name in self._groups:
            result[name] = self._get_group(name).to_dict()
        return result

    def to_namespace(self) -> types.SimpleNamespace:
        result: types.SimpleNamespace = types.SimpleNamespace()
        for name in self._fields:
            setattr(result, name, self._get_field(name).get())
        for name in self._groups:
            setattr(result, name, self._get_group(name).to_namespace())
        return result

    def _get_field(self, name: str) -> Var[Any]:
        return getattr(self, name)

    def _get_field_or_group(self, name: str) -> BaseConfig | Var[Any]:
        return getattr(self, name)

    def _get_group(self, name: str) -> BaseConfig:
        return getattr(self, name)
