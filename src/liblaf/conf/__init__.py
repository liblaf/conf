"""Expose the public configuration primitives for :mod:`liblaf.conf`.

The package centers on a small set of composable building blocks:

- :class:`BaseConfig` groups related settings behind a cached singleton.
- :class:`Field` binds one config attribute to a :class:`Var`.
- :func:`group` attaches nested config sections.
- :class:`Var` stores the active value in a :class:`contextvars.ContextVar`.

The ``field_*`` helper functions build common :class:`Field` variants with
converters for booleans, numbers, JSON payloads, paths, and temporal values.
"""

import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)
del lazy
