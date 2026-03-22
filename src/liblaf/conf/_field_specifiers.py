from __future__ import annotations

import datetime
import json
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pydantic

from ._field import Converter, Factory, Field
from ._sentinel import MISSING, MissingType

if TYPE_CHECKING:
    from _typeshed import StrPath


def field_bool(
    env: str | None = None,
    default: bool | MissingType = MISSING,  # noqa: FBT001
    factory: Factory[bool] | None = None,
    converter: Converter[bool] | None = None,
) -> Field[bool]:
    if converter is None:
        adapter: pydantic.TypeAdapter[bool] = pydantic.TypeAdapter(bool)
        converter: Converter[bool] = adapter.validate_python
    return Field(env=env, default=default, factory=factory, converter=converter)


def field_date(
    env: str | None = None,
    default: Any | MissingType = MISSING,
    factory: Factory[Any] | None = None,
    converter: Converter[Any] | None = None,
) -> Field[Any]:
    if converter is None:
        adapter: pydantic.TypeAdapter[datetime.date] = pydantic.TypeAdapter(
            datetime.date
        )
        converter: Converter[Any] = adapter.validate_python
    return Field(env=env, default=default, factory=factory, converter=converter)


def field_datetime(
    env: str | None = None,
    default: datetime.datetime | MissingType = MISSING,
    factory: Factory[datetime.datetime] | None = None,
    converter: Converter[datetime.datetime] | None = None,
) -> Field[datetime.datetime]:
    if converter is None:
        adapter: pydantic.TypeAdapter[datetime.datetime] = pydantic.TypeAdapter(
            datetime.datetime
        )
        converter: Converter[datetime.datetime] = adapter.validate_python
    return Field(env=env, default=default, factory=factory, converter=converter)


def field_decimal(
    env: str | None = None,
    default: Decimal | MissingType = MISSING,
    factory: Factory[Decimal] | None = None,
    converter: Converter[Decimal] | None = None,
) -> Field[Decimal]:
    if converter is None:
        converter: Converter[Decimal] = Decimal
    return Field(env=env, default=default, factory=factory, converter=converter)


def field_float(
    env: str | None = None,
    default: float | MissingType = MISSING,
    factory: Factory[float] | None = None,
    converter: Converter[float] | None = None,
) -> Field[float]:
    if converter is None:
        converter: Converter[float] = float
    return Field(env=env, default=default, factory=factory, converter=converter)


def field_int(
    env: str | None = None,
    default: int | MissingType = MISSING,
    factory: Factory[int] | None = None,
    converter: Converter[int] | None = None,
) -> Field[int]:
    if converter is None:
        converter: Converter[int] = int
    return Field(env=env, default=default, factory=factory, converter=converter)


def field_json(
    env: str | None = None,
    default: Any | MissingType = MISSING,
    factory: Factory[Any] | None = None,
    converter: Converter[Any] | None = None,
) -> Field[Any]:
    if converter is None:
        converter: Converter[Any] = json.loads
    return Field(env=env, default=default, factory=factory, converter=converter)


def field_list_str(
    env: str | None = None,
    default: list[str] | MissingType = MISSING,
    factory: Factory[list[str]] | None = None,
    converter: Converter[list[str]] | None = None,
    delimiter: str = ",",
) -> Field[list[str]]:
    if converter is None:

        def converter(value: str) -> list[str]:
            return [item.strip() for item in value.split(delimiter)]

    return Field(env=env, default=default, factory=factory, converter=converter)


def field_path(
    env: str | None = None,
    default: StrPath | MissingType = MISSING,
    factory: Factory[StrPath] | None = None,
    converter: Converter[Path] | None = None,
) -> Field[Path]:
    if converter is None:
        converter: Converter[Path] = Path
    if default is not MISSING:
        default = Path(default)
    if factory is not None:
        wrapped: Factory[StrPath] = factory

        def factory() -> Path:
            return Path(wrapped())

    return Field(env=env, default=default, factory=factory, converter=converter)


def field_str(
    env: str | None = None,
    default: str | MissingType = MISSING,
    factory: Factory[str] | None = None,
    converter: Converter[str] | None = None,
) -> Field[str]:
    return Field(env=env, default=default, factory=factory, converter=converter)


def field_time(
    env: str | None = None,
    default: datetime.time | MissingType = MISSING,
    factory: Factory[datetime.time] | None = None,
    converter: Converter[datetime.time] | None = None,
) -> Field[datetime.time]:
    if converter is None:
        adapter: pydantic.TypeAdapter[datetime.time] = pydantic.TypeAdapter(
            datetime.time
        )
        converter: Converter[datetime.time] = adapter.validate_python
    return Field(env=env, default=default, factory=factory, converter=converter)


def field_timedelta(
    env: str | None = None,
    default: datetime.timedelta | MissingType = MISSING,
    factory: Factory[datetime.timedelta] | None = None,
    converter: Converter[datetime.timedelta] | None = None,
) -> Field[datetime.timedelta]:
    if converter is None:
        adapter: pydantic.TypeAdapter[datetime.timedelta] = pydantic.TypeAdapter(
            datetime.timedelta
        )
        converter: Converter[datetime.timedelta] = adapter.validate_python
    return Field(env=env, default=default, factory=factory, converter=converter)
