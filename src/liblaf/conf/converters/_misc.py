"""Small converter helpers that do not depend on third-party validators."""


def identity[T](x: T) -> T:
    """Return a value unchanged.

    This is the default converter for fields and variables that already receive
    values in their final Python form.
    """
    return x
