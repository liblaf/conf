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
    calls: list[int] = []

    def build() -> list[int]:
        calls.append(1)
        return []

    var: conf.Var[list[int]] = conf.Var("items", factory=build)
    assert var.get() == []
    assert calls == [1]


def test_var_without_value_raises_unless_default_is_provided() -> None:
    var: conf.Var[list] = conf.Var("items", factory=list)
    missing: conf.Var[str] = conf.Var("missing")

    assert var.name == "items"
    assert var.get() == []
    assert missing.get("fallback") == "fallback"
    with pytest.raises(LookupError):
        missing.get()


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


def test_var_load_env_ignores_missing_or_unconfigured_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    configured: conf.Var[str] = conf.Var("configured", default="local", env="APP_MODE")
    unconfigured: conf.Var[str] = conf.Var("unconfigured", default="local")

    configured.load_env()
    unconfigured.load_env()
    assert configured.get() == "local"
    assert unconfigured.get() == "local"

    monkeypatch.setenv("APP_MODE", "prod")
    configured.load_env()
    assert configured.get() == "prod"


def test_var_reloads_missing_environment_to_a_fresh_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def converter(value: str | list[str]) -> list[str]:
        return [value] if isinstance(value, str) else value

    var: conf.Var[list[str]] = conf.Var(
        "labels", default=["default"], env="APP_LABELS", converter=converter
    )
    var.set(["explicit"])
    monkeypatch.setenv("APP_LABELS", "environment")
    var.load_env()
    assert var.get() == ["environment"]

    monkeypatch.delenv("APP_LABELS")
    var.load_env()
    assert var.get() == ["default"]


def test_var_defaults_are_fresh_in_each_context_and_set_uses_converter() -> None:
    var: conf.Var[list[str]] = conf.Var(
        "labels",
        default=["default"],
        converter=lambda value: [item.upper() for item in value],
    )
    assert var.get() == ["DEFAULT"]
    var.get().append("LOCAL")

    other_context = contextvars.Context()
    assert other_context.run(var.get) == ["DEFAULT"]
    assert var.get() == ["DEFAULT", "LOCAL"]

    var.set(["direct"])
    assert var.get() == ["DIRECT"]


def test_var_override_is_context_local() -> None:
    var: conf.Var[str] = conf.Var("mode", default="global")
    other_context: contextvars.Context = contextvars.Context()

    with var.override("local"):
        assert var.get() == "local"
        assert other_context.run(var.get) == "global"
    assert var.get() == "global"
