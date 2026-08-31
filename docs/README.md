# conf

Define configuration as ordinary Python classes, bind fields to environment
variables, and override values for the current `contextvars` context.

```bash
uv add liblaf-conf
```

`liblaf-conf` supports Python 3.12 and newer.

## Define Settings

Subclass `BaseConfig`, declare values with `Field` or a `field_*` helper, and
compose nested sections with `group()`.

```python
from liblaf import conf


class DatabaseConfig(conf.BaseConfig):
    url: conf.Field[str] = conf.field_str(default="sqlite:///app.db")


class AppConfig(conf.BaseConfig):
    debug: conf.Field[bool] = conf.field_bool(default=False)
    port: conf.Field[int] = conf.field_int(env="PORT", default=8000)
    hosts: conf.Field[list[str]] = conf.field_list_str(factory=lambda: ["localhost"])
    database: conf.Group[DatabaseConfig] = conf.group(DatabaseConfig)
```

`AppConfig()` is a cached singleton. Accessing `cfg.port` returns a `Var`, and
that variable stores its active value in a `ContextVar`.

## Load, Set, and Override

Call `load_env()` when string values should come from the environment. Call
`set()` when you already have Python values. For nested groups, pass nested
mappings.

```python
cfg = AppConfig()

cfg.load_env()
cfg.set(database={"url": "sqlite:///dev.db"})

with cfg.override(debug=True, database={"url": "sqlite:///test.db"}):
    assert cfg.debug.get() is True
    assert cfg.database.url.get() == "sqlite:///test.db"

assert cfg.database.url.get() == "sqlite:///dev.db"
```

Use the field `Var` directly when only one value needs to change.

```python
token = cfg.port.set(9000)
try:
    assert cfg.port.get() == 9000
finally:
    cfg.port.reset(token)
```

## Convert Environment Strings

Environment variables are strings, so each field can carry a converter. The
helper constructors cover common cases:

- `field_bool`, `field_int`, `field_float`, `field_decimal`, and `field_str`
  for scalar values.
- `field_json`, `field_list_str`, and `field_path` for structured values.
- `field_date`, `field_datetime`, `field_time`, and `field_timedelta` for
  temporal values backed by Pydantic validation.

```python
class WorkerConfig(conf.BaseConfig):
    retries: conf.Field[int] = conf.field_int(default=3)
    labels: conf.Field[list[str]] = conf.field_list_str(delimiter=";")
```

For lower-level control, pass your own converter to `field()`, `Field`, or
`Var`.

## Serialize the Active State

Use `to_dict()` when another library needs ordinary dictionaries. Use
`to_namespace()` when attribute access is more convenient.

```python
cfg.set(port=8000, debug=True, hosts=["localhost", "example.test"])

assert cfg.to_dict() == {
    "debug": True,
    "port": 8000,
    "hosts": ["localhost", "example.test"],
    "database": {"url": "sqlite:///dev.db"},
}
```

`to_dict()` reads the same active context as `get()`, so temporary overrides
are reflected while the override is active and disappear when it exits.

## Context and Reload Semantics

`load_env()`, `set()`, and `override()` operate in the current `ContextVar`
context. Tasks inherit a context when created; later changes do not mutate
existing tasks or other threads. `to_dict()` returns new dictionaries and
`to_namespace()` returns new namespace containers, but neither deep-copies
mutable field values. Copy a mutable leaf yourself when a downstream boundary
requires ownership or immutability.

Each reload is complete for the active context: a present environment variable
is converted and installed, while an absent one clears the active value and
returns the field to a fresh default or factory result on the next read.
`set()` and `override()` pass their Python values through the same converter.
Invalid values raise their conversion error; no fallback value is substituted.

## API Map

- [liblaf.conf](reference/liblaf/conf/README.md): config containers, fields,
  groups, variables, and `field_*` helpers.
- [liblaf.conf.converters](reference/liblaf/conf/converters/README.md):
  Pydantic-backed converter factories and `identity`.
