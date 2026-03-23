from liblaf import conf


def test_config_meta_generates_name_env_prefix_and_updates_mro_maps() -> None:
    class BaseSettings(conf.BaseConfig):
        inherited: conf.Field[int] = conf.Field(default=1)
        nested: conf.Group[dict] = conf.group(lambda: {"source": "base"})

    class AppConfig(BaseSettings):
        inherited = "removed"
        nested: conf.Field[str] = conf.Field(default="local")
        extra: conf.Field[int] = conf.Field(default=2)

    assert AppConfig.name == "app"
    assert AppConfig.env_prefix == "APP_"
    assert list(AppConfig._fields) == ["nested", "extra"]
    assert AppConfig._groups == {}  # noqa: SLF001


def test_config_meta_returns_singleton_and_calls_init_once() -> None:
    calls: list[str] = []

    class SingletonConfig(conf.BaseConfig):
        def __init__(self) -> None:
            calls.append("init")

    assert SingletonConfig() is SingletonConfig()
    assert calls == ["init"]
