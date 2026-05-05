from __future__ import annotations

from typing import cast

import pydantic

from liblaf.conf import converters


class Model(pydantic.BaseModel):
    count: int
    flag: bool = False


def test_identity_returns_same_object() -> None:
    value: object = object()

    assert converters.identity(value) is value


def test_pydantic_model_converter_helpers() -> None:
    validate_python = converters.pydantic_model_validate(Model)
    validate_json = converters.pydantic_model_validate_json(Model)
    validate_strings = converters.pydantic_model_validate_strings(Model)

    assert validate_python(cast("str", {"count": "1"})).count == 1
    assert validate_json('{"count": 2, "flag": true}').flag is True
    assert validate_strings(cast("str", {"count": "3", "flag": "true"})) == Model(
        count=3, flag=True
    )


def test_pydantic_type_adapter_converter_helpers() -> None:
    validate_python = converters.pydantic_type_adapter_validate_python(list[int])
    validate_json = converters.pydantic_type_adapter_validate_json(list[int])
    validate_strings = converters.pydantic_type_adapter_validate_strings(bool)

    assert validate_python(cast("str", ["1", 2])) == [1, 2]
    assert validate_json("[1, 2]") == [1, 2]
    assert validate_strings("true") is True
