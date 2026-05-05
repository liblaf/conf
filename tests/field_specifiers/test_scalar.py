from collections.abc import Callable
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from liblaf import conf


@pytest.mark.parametrize(
    ("factory", "value", "expected"),
    [
        (conf.field_bool, "true", True),
        (conf.field_decimal, "3.14", Decimal("3.14")),
        (conf.field_float, "2.5", 2.5),
        (conf.field_int, "42", 42),
        (conf.field_str, "hello", "hello"),
        (conf.field_path, "folder/file.txt", Path("folder/file.txt")),
    ],
)
def test_scalar_field_specifiers_convert_values[T](
    factory: Callable[[], conf.Field[T]], value: str, expected: T
) -> None:
    field: conf.Field[T] = factory()
    assert field.converter(value) == expected


def test_scalar_field_specifiers_accept_custom_converter() -> None:
    field: conf.Field[int] = conf.field_int(converter=len)

    assert field.converter("abc") == 3


@pytest.mark.parametrize(
    "factory",
    [
        conf.field_bool,
        conf.field_date,
        conf.field_datetime,
        conf.field_decimal,
        conf.field_float,
        conf.field_int,
        conf.field_json,
        conf.field_list_str,
        conf.field_path,
        conf.field_str,
        conf.field_time,
        conf.field_timedelta,
    ],
)
def test_field_specifiers_use_custom_converter(
    factory: Callable[..., conf.Field[Any]],
) -> None:
    calls: list[str] = []

    def converter(value: str) -> str:
        calls.append(value)
        return f"converted:{value}"

    field: conf.Field[Any] = factory(converter=converter)

    assert field.converter("value") == "converted:value"
    assert calls == ["value"]


def test_field_path_converts_default_and_factory_values() -> None:
    default_field: conf.Field[Path] = conf.field_path(default="cache")
    factory_field: conf.Field[Path] = conf.field_path(factory=lambda: "state")

    assert default_field.default == Path("cache")
    assert factory_field.factory is not None
    assert factory_field.factory() == Path("state")
