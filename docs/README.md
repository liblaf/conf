# conf

`liblaf-conf` helps you keep application configuration in normal Python classes
instead of a tangle of globals, nested dicts, and ad hoc parsing code. The
package combines descriptor-based declarations, environment-variable loading,
and `contextvars`-backed overrides so the active configuration stays explicit
and test-friendly.

## A Small Working Example

```python
from liblaf import conf


class DatabaseConfig(conf.BaseConfig):
    url: conf.Field[str] = conf.field_str(default="sqlite:///app.db")


class AppConfig(conf.BaseConfig):
    debug: conf.Field[bool] = conf.field_bool(default=False)
    allowed_hosts: conf.Field[list[str]] = conf.field_list_str(default=["localhost"])
    database: conf.Group[DatabaseConfig] = conf.group(DatabaseConfig)


cfg = AppConfig()
cfg.set(database={"url": "sqlite:///dev.db"})
cfg.load_env()

with cfg.override(debug=True):
    assert cfg.debug.get() is True
```

This is the full shape of the library: define config with `BaseConfig`, attach
values with `Field`, compose sections with `group()`, and let each bound `Var`
manage the active value.

The package centers on four building blocks:

- `BaseConfig` groups related settings and exposes serialization helpers.
- `Field` declares one config value and binds it to a `Var`.
- `group()` attaches nested config sections.
- `Var` stores the active value and supports `get()`, `set()`, `load_env()`,
  and `override()`.

## Start Here

Install the package with `uv`:

```bash
uv add liblaf-conf
```

`liblaf-conf` supports Python 3.12 and newer.

If you want the shortest path from declaration to use, start with these
operations:

- Declare settings with `Field(...)` or a `field_*` helper.
- Compose nested sections with `group(...)`.
- Call `set(...)` for Python-side updates and `load_env()` for environment
  values.
- Use `override(...)` for temporary changes and `to_dict()` or
  `to_namespace()` when you need to serialize the active state.

Here is a slightly fuller example that shows serialization as well:

```python
from liblaf import conf


class DatabaseConfig(conf.BaseConfig):
    url: conf.Field[str] = conf.field_str(default="sqlite:///app.db")


class AppConfig(conf.BaseConfig):
    debug: conf.Field[bool] = conf.field_bool(default=False)
    allowed_hosts: conf.Field[list[str]] = conf.field_list_str(default=["localhost"])
    database: conf.Group[DatabaseConfig] = conf.group(DatabaseConfig)


cfg = AppConfig()
cfg.set(debug=True, database={"url": "sqlite:///dev.db"})

assert cfg.to_dict() == {
    "debug": True,
    "allowed_hosts": ["localhost"],
    "database": {"url": "sqlite:///dev.db"},
}
```

## Choosing an API

Reach for `Field(...)` when you want to set a default, use a factory, override
the generated environment-variable name, or provide your own converter.

Use the `field_*` helpers when the value is already one of the supported scalar,
structured, or temporal types and you want the package to provide the
conversion logic.

Use `group()` when one config section should own another config section and you
want `set()`, `load_env()`, `to_dict()`, and `override()` to recurse through
the whole tree.

## Where To Go Next

- Read the [API reference overview](reference/README.md) for the reference map.
- Open [Core primitives](reference/core.md) for `BaseConfig`, `Field`, `Var`,
  `field()`, and `group()`.
- Open [Field helpers](reference/field-helpers.md) for the `field_*`
  convenience factories.
- Open [Converters](reference/converters.md) when you want lower-level
  Pydantic-backed converter helpers.
- Visit the [GitHub repository](https://github.com/liblaf/conf) for release
  notes, issue tracking, and development workflow details.
