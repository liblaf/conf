import types

import pytest

from liblaf import conf


def test_base_config_set_override_and_serializers_work_with_groups() -> None:
    class ChildConfig(conf.BaseConfig):
        flag: conf.Field[bool] = conf.Field(default=False)

    class AppConfig(conf.BaseConfig):
        count: conf.Field[int] = conf.Field(default=1)
        child: conf.Group[ChildConfig] = conf.group(ChildConfig)

    cfg = AppConfig()
    cfg.set({"count": 7, "child": {"flag": True}})

    namespace: types.SimpleNamespace = cfg.to_namespace()
    assert cfg.to_dict() == {"count": 7, "child": {"flag": True}}
    assert namespace.count == 7
    assert namespace.child.flag is True

    with cfg.override(count=9, child={"flag": False}):
        assert cfg.to_dict() == {"count": 9, "child": {"flag": False}}
    assert cfg.to_dict() == {"count": 7, "child": {"flag": True}}


def test_base_config_override_restores_values_after_exception() -> None:
    class AppConfig(conf.BaseConfig):
        count: conf.Field[int] = conf.Field(default=1)

    cfg = AppConfig()

    def fail_inside_override() -> None:
        with cfg.override(count=2):
            assert cfg.count.get() == 2
            message = "boom"
            raise RuntimeError(message)

    with pytest.raises(RuntimeError, match="boom"):
        fail_inside_override()

    assert cfg.count.get() == 1


def test_base_config_rejects_unknown_set_or_override_names() -> None:
    class AppConfig(conf.BaseConfig):
        count: conf.Field[int] = conf.Field(default=1)

    cfg = AppConfig()

    with pytest.raises(AttributeError):
        cfg.set(missing=True)
    with pytest.raises(AttributeError), cfg.override(missing=True):
        pass


def test_base_config_mapping_values_take_precedence_over_kwargs() -> None:
    class AppConfig(conf.BaseConfig):
        count: conf.Field[int] = conf.Field(default=1)

    cfg = AppConfig()
    cfg.set({"count": 3}, count=2)

    assert cfg.count.get() == 3


def test_base_config_load_env_recurses_into_groups(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_COUNT", "5")
    monkeypatch.setenv("CHILD_FLAG", "1")

    class ChildConfig(conf.BaseConfig):
        flag: conf.Field[bool] = conf.Field(
            default=False, converter=lambda value: value == "1"
        )

    class AppConfig(conf.BaseConfig):
        count: conf.Field[int] = conf.Field(default=1, env="APP_COUNT", converter=int)
        child: conf.Group[ChildConfig] = conf.group(ChildConfig)

    cfg = AppConfig()
    cfg.load_env()

    assert cfg.to_dict() == {"count": 5, "child": {"flag": True}}


def test_base_config_set_and_override_use_field_converter() -> None:
    class AppConfig(conf.BaseConfig):
        count: conf.Field[int] = conf.Field(default=1, converter=int)

    cfg = AppConfig()
    cfg.set(count="2")
    assert cfg.count.get() == 2
    with cfg.override(count="3"):
        assert cfg.count.get() == 3
    with pytest.raises(ValueError, match="invalid literal"):
        cfg.set(count="not-an-int")
