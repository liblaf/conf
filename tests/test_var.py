import contextvars

import pytest

from liblaf import conf


def test_var_uses_environment_and_converter_at_creation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_PORT", "42")
    var: conf.Var[int] = conf.Var("port", default=1, env="APP_PORT", converter=int)

    assert var.get() == 42
    assert var.env == "APP_PORT"
    assert var.converter is int


def test_var_uses_factory_and_default_fallback() -> None:
    var: conf.Var[list] = conf.Var("items", factory=list)
    missing: conf.Var[str] = conf.Var("missing")

    assert var.name == "items"
    assert var.get() == []
    assert missing.get("fallback") == "fallback"


def test_var_load_env_reset_and_override_restore_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    var: conf.Var[str] = conf.Var("mode", default="dev", env="APP_MODE")
    monkeypatch.setenv("APP_MODE", "prod")

    var.load_env()
    assert var.get() == "prod"

    token: contextvars.Token[str] = var.set("test")
    assert var.get() == "test"
    var.reset(token)
    assert var.get() == "prod"

    with var.override("local"):
        assert var.get() == "local"
    assert var.get() == "prod"
