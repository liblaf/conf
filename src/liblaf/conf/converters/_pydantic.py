from __future__ import annotations

from typing import TYPE_CHECKING

import pydantic

if TYPE_CHECKING:
    from liblaf.conf._field import Converter


def pydantic_model_validate[T: pydantic.BaseModel](model: type[T]) -> Converter[T]:
    return model.model_validate


def pydantic_model_validate_json[T: pydantic.BaseModel](model: type[T]) -> Converter[T]:
    return model.model_validate_json


def pydantic_model_validate_strings[T: pydantic.BaseModel](
    model: type[T],
) -> Converter[T]:
    return model.model_validate_strings


def pydantic_type_adapter_validate_json[T](type_: type[T]) -> Converter[T]:
    return pydantic.TypeAdapter(type_).validate_json


def pydantic_type_adapter_validate_python[T](type_: type[T]) -> Converter[T]:
    return pydantic.TypeAdapter(type_).validate_python


def pydantic_type_adapter_validate_strings[T](type_: type[T]) -> Converter[T]:
    return pydantic.TypeAdapter(type_).validate_strings
