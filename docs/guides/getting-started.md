# Getting started

Define a `BaseConfig` subclass and annotate every descriptor with `Field` or a
specialized `field_*` factory. Instantiating the class returns its cached config
object; accessing a field returns its context-local `Var`.

```python
from liblaf import conf


class AppConfig(conf.BaseConfig):
    debug: conf.Field[bool] = conf.field_bool(default=False)
    port: conf.Field[int] = conf.field_int(env="PORT", default=8000)


config = AppConfig()
config.load_env()
config.set(debug=True)
assert config.port.get() == 8000
```

Use `get()` to read a field, `set()` for persistent changes in the current
context, and `override()` for a scoped temporary change.
