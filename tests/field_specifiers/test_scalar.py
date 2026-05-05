from collections.abc import Callable
from decimal import Decimal
from pathlib import Path

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


def test_field_path_converts_default_and_factory_values() -> None:
    default_field: conf.Field[Path] = conf.field_path(default="cache")
    factory_field: conf.Field[Path] = conf.field_path(factory=lambda: "state")

    assert default_field.default == Path("cache")
    assert factory_field.factory is not None
    assert factory_field.factory() == Path("state")
