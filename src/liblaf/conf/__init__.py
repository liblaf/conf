"""Typed configuration primitives with environment loading and scoped overrides.

The public API is intentionally small:

- [`BaseConfig`][liblaf.conf.BaseConfig] groups related settings behind a
  cached singleton.
- [`Field`][liblaf.conf.Field] declares one setting and binds it to a
  [`Var`][liblaf.conf.Var] on first access.
- [`group`][liblaf.conf.group] attaches nested configuration sections.
- [`Var`][liblaf.conf.Var] stores the active value in a
  [`contextvars.ContextVar`][].

The `field_*` helpers create [`Field`][liblaf.conf.Field] descriptors with
ready-made converters for booleans, numbers, JSON payloads, paths, lists, and
temporal values.
"""

import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)
del lazy
