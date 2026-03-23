import enum


class MissingType(enum.Enum):
    MISSING = enum.auto()


MISSING: MissingType = MissingType.MISSING
