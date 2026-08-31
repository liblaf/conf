# Environment reload

Field environment names default to `<ENV_PREFIX><FIELD_NAME>`, where the prefix
comes from the config class name. Pass `env=` to a field factory for an explicit
name.

`load_env()` refreshes every field and nested group in the active context. If a
configured variable is present, its string is converted and stored. If it is
absent, the active value is cleared; the next `get()` materializes a fresh
declared default or factory value. Reloading never retains a stale earlier
environment value.

```python
from liblaf import conf


class ServerConfig(conf.BaseConfig):
    port: conf.Field[int] = conf.field_int(env="PORT", default=8000)
```

Set `PORT=9000` before `ServerConfig().load_env()` to install `9000`. Invalid
strings raise the converter error.
