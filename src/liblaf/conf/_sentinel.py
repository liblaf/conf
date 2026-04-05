"""Sentinel values shared by configuration primitives."""

import enum


class MissingType(enum.Enum):
    """Sentinel enum used to distinguish an omitted default from `None`."""

    MISSING = enum.auto()


MISSING: MissingType = MissingType.MISSING
