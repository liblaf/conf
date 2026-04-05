# conf

`liblaf-conf` helps you define application configuration as typed descriptors
backed by `contextvars`. It is aimed at Python projects that want a compact API
for defaults, environment-variable loading, nested config sections, and scoped
runtime overrides.

The package centers on four building blocks:

- `BaseConfig` groups related settings and exposes serialization helpers.
- `Field` declares one config value and binds it to a `Var`.
- `group()` attaches nested config sections.
- `Var` stores the active value and supports `get()`, `set()`, `load_env()`,
  and `override()`.

## Start Here

The README contains the quickest path from declaration to use:

--8<-- "README.md"

## Choosing an API

Reach for `Field(...)` when you want to configure a default, a factory, an
explicit environment variable name, or a custom converter yourself.

Use the `field_*` helpers when the value is already one of the supported scalar,
structured, or temporal types and you want the package to provide the
conversion logic.

Use `group()` when one config section should own another config section.

## Next Step

The generated reference documents every exported symbol, including the
converter helpers:

- [API reference](reference/README.md)
