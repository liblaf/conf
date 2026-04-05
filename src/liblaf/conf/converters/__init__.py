"""Expose converter helpers used by :mod:`liblaf.conf` fields and variables.

Most applications will reach for the higher-level ``field_*`` helpers first.
This module is the lower-level escape hatch for cases where you want to pass a
converter directly to :class:`liblaf.conf.Field` or :class:`liblaf.conf.Var`.

The exported helpers either leave values unchanged or delegate validation to
Pydantic models and type adapters.
"""

import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)
del lazy
