"""Converter factories built on top of Pydantic validation APIs."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pydantic

if TYPE_CHECKING:
    from liblaf.conf._types import Converter


def pydantic_model_validate[T: pydantic.BaseModel](model: type[T]) -> Converter[T]:
    """Return a converter that validates Python objects against a model.

    Args:
        model: The Pydantic model class used to validate incoming objects.

    Returns:
        A callable suitable for ``Field(converter=...)`` or ``Var`` that
        delegates to ``model.model_validate``.
    """
    return model.model_validate


def pydantic_model_validate_json[T: pydantic.BaseModel](model: type[T]) -> Converter[T]:
    """Return a converter that validates JSON strings against a model.

    Args:
        model: The Pydantic model class used to parse JSON payloads.

    Returns:
        A callable that delegates to ``model.model_validate_json``.
    """
    return model.model_validate_json


def pydantic_model_validate_strings[T: pydantic.BaseModel](
    model: type[T],
) -> Converter[T]:
    """Return a converter that validates string inputs against a model.

    Args:
        model: The Pydantic model class used to coerce string-based inputs.

    Returns:
        A callable that delegates to ``model.model_validate_strings``.
    """
    return model.model_validate_strings


def pydantic_type_adapter_validate_json[T](type_: type[T]) -> Converter[T]:
    """Return a converter that validates JSON strings for an arbitrary type.

    Args:
        type_: The target Python type validated by ``pydantic.TypeAdapter``.

    Returns:
        A callable that parses JSON strings into ``type_`` values.
    """
    return pydantic.TypeAdapter(type_).validate_json


def pydantic_type_adapter_validate_python[T](type_: type[T]) -> Converter[T]:
    """Return a converter that validates Python objects for an arbitrary type.

    Args:
        type_: The target Python type validated by ``pydantic.TypeAdapter``.

    Returns:
        A callable that validates already-parsed Python objects.
    """
    return pydantic.TypeAdapter(type_).validate_python


def pydantic_type_adapter_validate_strings[T](type_: type[T]) -> Converter[T]:
    """Return a converter that validates string inputs for an arbitrary type.

    Args:
        type_: The target Python type validated by ``pydantic.TypeAdapter``.

    Returns:
        A callable that coerces string inputs into ``type_`` values.
    """
    return pydantic.TypeAdapter(type_).validate_strings
