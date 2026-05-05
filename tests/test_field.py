import pytest

from liblaf import conf


def test_field_descriptor_returns_self_on_class_and_binds_once() -> None:
    class SampleConfig(conf.BaseConfig):
        value: conf.Field[int] = conf.Field(default=1)

    cfg = SampleConfig()

    assert SampleConfig.value is SampleConfig.__dict__["value"]
    assert cfg.value is cfg.value
    assert cfg.value.name == "sample.value"
    assert cfg.value.env == "SAMPLE_VALUE"
    assert cfg.value.get() == 1


def test_field_uses_explicit_env_and_converter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CUSTOM_COUNT", "5")

    class SampleConfig(conf.BaseConfig):
        value: conf.Field[int] = conf.Field(env="CUSTOM_COUNT", converter=int)

    cfg = SampleConfig()

    assert cfg.value.env == "CUSTOM_COUNT"
    assert cfg.value.get() == 5


def test_field_passes_factory_to_bound_var() -> None:
    calls: list[int] = []

    def build() -> list[int]:
        calls.append(1)
        return []

    class SampleConfig(conf.BaseConfig):
        items: conf.Field[list[int]] = conf.Field(factory=build)

    assert SampleConfig().items.get() == []
    assert calls == [1]


def test_field_helper_builds_descriptor_with_defaults() -> None:
    field: conf.Field[str] = conf.field(default="fallback", env="VALUE")

    assert field.default == "fallback"
    assert field.env == "VALUE"
    assert field.converter("env-value") == "env-value"
