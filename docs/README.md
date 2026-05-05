# conf

`liblaf-conf` is a small descriptor-based configuration layer for Python
applications. You declare settings as normal classes, load string values from
environment variables, and use `contextvars`-backed overrides when tests,
tasks, or request handlers need a temporary view of configuration.

## Install

```bash
uv add liblaf-conf
```

`liblaf-conf` supports Python 3.12 and newer.

## Define a Config Tree

Start with `BaseConfig`. Add scalar settings with `Field` or a `field_*`
helper, then compose nested sections with `group()`.

```python
from liblaf import conf


class DatabaseConfig(conf.BaseConfig):
    url: conf.Field[str] = conf.field_str(default="sqlite:///app.db")


class AppConfig(conf.BaseConfig):
    debug: conf.Field[bool] = conf.field_bool(default=False)
    port: conf.Field[int] = conf.field_int(env="PORT", default=8000)
    hosts: conf.Field[list[str]] = conf.field_list_str(default=["localhost"])
    database: conf.Group[DatabaseConfig] = conf.group(DatabaseConfig)
```

`AppConfig()` returns a cached singleton. Each field still stores its active
value in a `Var`, so overrides are scoped to the current `contextvars` context
instead of mutating a process-wide global forever.

## Load, Set, and Override

Call `load_env()` to refresh every field from its configured environment
variable. Call `set()` when you already have Python values, and pass nested
mappings for nested config groups.

```python
cfg = AppConfig()

cfg.load_env()
cfg.set(database={"url": "sqlite:///dev.db"})

with cfg.override(debug=True, database={"url": "sqlite:///test.db"}):
    assert cfg.debug.get() is True
    assert cfg.database.url.get() == "sqlite:///test.db"

assert cfg.database.url.get() == "sqlite:///dev.db"
```

Fields expose `Var` objects. Use `get()`, `set()`, `reset()`, `load_env()`,
and `override()` directly when you only need to work with one value.

```python
token = cfg.port.set(9000)
try:
    assert cfg.port.get() == 9000
finally:
    cfg.port.reset(token)
```

## Convert Environment Strings

`Field` accepts any converter callable. The convenience helpers cover common
cases:

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

## API Map

- [liblaf.conf](reference/liblaf/conf/README.md): config containers, fields,
  groups, variables, and `field_*` helpers.
- [liblaf.conf.converters](reference/liblaf/conf/converters/README.md):
  Pydantic-backed converter factories and `identity`.
