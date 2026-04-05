"""Converter factories built on top of Pydantic validation APIs."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pydantic

if TYPE_CHECKING:
    from liblaf.conf._types import Converter


def pydantic_model_validate[T: pydantic.BaseModel](model: type[T]) -> Converter[T]:
    """Return a converter that validates Python objects against a model."""
    return model.model_validate


def pydantic_model_validate_json[T: pydantic.BaseModel](model: type[T]) -> Converter[T]:
    """Return a converter that validates JSON strings against a model."""
    return model.model_validate_json


def pydantic_model_validate_strings[T: pydantic.BaseModel](
    model: type[T],
) -> Converter[T]:
    """Return a converter that validates string inputs against a model."""
    return model.model_validate_strings


def pydantic_type_adapter_validate_json[T](type_: type[T]) -> Converter[T]:
    """Return a converter that validates JSON strings for an arbitrary type."""
    return pydantic.TypeAdapter(type_).validate_json


def pydantic_type_adapter_validate_python[T](type_: type[T]) -> Converter[T]:
    """Return a converter that validates Python objects for an arbitrary type."""
    return pydantic.TypeAdapter(type_).validate_python


def pydantic_type_adapter_validate_strings[T](type_: type[T]) -> Converter[T]:
    """Return a converter that validates string inputs for an arbitrary type."""
    return pydantic.TypeAdapter(type_).validate_strings
