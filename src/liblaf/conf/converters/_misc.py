"""Small converter helpers that do not depend on third-party validators."""


def identity[T](x: T) -> T:
    """Return the input unchanged."""
    return x
