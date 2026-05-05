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


def test_config_meta_preserves_explicit_names_and_inherited_order() -> None:
    class RootConfig(conf.BaseConfig):
        name = "root"
        env_prefix = "ROOTS_"
        first: conf.Field[int] = conf.Field(default=1)

    class BranchConfig(RootConfig):
        second: conf.Field[int] = conf.Field(default=2)

    assert RootConfig.name == "root"
    assert RootConfig.env_prefix == "ROOTS_"
    assert BranchConfig.name == "branch"
    assert BranchConfig.env_prefix == "BRANCH_"
    assert list(BranchConfig._fields) == ["first", "second"]
    assert BranchConfig().first.env == "BRANCH_FIRST"
    assert BranchConfig().second.name == "branch.second"


def test_config_meta_removes_inherited_descriptor_replaced_by_plain_attribute() -> None:
    class RootConfig(conf.BaseConfig):
        enabled: conf.Field[bool] = conf.Field(default=True)

    class BranchConfig(RootConfig):
        enabled = False

    assert BranchConfig._fields == {}
    assert BranchConfig().enabled is False


def test_config_meta_returns_singleton_and_calls_init_once() -> None:
    calls: list[str] = []

    class SingletonConfig(conf.BaseConfig):
        def __init__(self) -> None:
            calls.append("init")

    assert SingletonConfig() is SingletonConfig()
    assert calls == ["init"]
