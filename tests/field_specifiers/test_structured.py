from typing import Any

from liblaf import conf


def test_field_json() -> None:
    field: conf.Field[Any] = conf.field_json()
    assert field.converter('{"key": "value"}') == {"key": "value"}


def test_field_list_str() -> None:
    field: conf.Field[list[str]] = conf.field_list_str(delimiter="|")
    assert field.converter("a | b|c") == ["a", "b", "c"]


def test_field_list_str_keeps_empty_items() -> None:
    field: conf.Field[list[str]] = conf.field_list_str()

    assert field.converter("a,, b,") == ["a", "", "b", ""]
