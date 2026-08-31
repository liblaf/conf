# Testing configuration

Use `override()` to confine a test setting to one block and guarantee cleanup:

```python
config = AppConfig()

with config.override(debug=True):
    assert config.debug.get() is True

assert config.debug.get() is False
```

Use `monkeypatch.setenv()` followed by `load_env()` when exercising environment
behavior. Give test-local config classes distinct names: each `BaseConfig`
subclass is a singleton for the lifetime of its Python class, while values are
still context-local.
