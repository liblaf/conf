from liblaf import conf
from liblaf.conf._group import Group, group


def test_group_descriptor_returns_self_and_caches_factory_result() -> None:
    calls: list[int] = []

    def build() -> dict[str, int]:
        calls.append(1)
        return {"count": len(calls)}

    class SampleConfig(conf.BaseConfig):
        nested = Group(build)

    cfg = SampleConfig()
    first = cfg.nested
    second = cfg.nested

    assert SampleConfig.nested is SampleConfig.__dict__["nested"]
    assert first is second
    assert first == {"count": 1}
    assert calls == [1]


def test_group_helper_wraps_nested_configs() -> None:
    class ChildConfig(conf.BaseConfig):
        value: conf.Field[int] = conf.Field(default=1)

    class ParentConfig(conf.BaseConfig):
        child = group(ChildConfig)

    cfg = ParentConfig()

    assert isinstance(ParentConfig.__dict__["child"], Group)
    assert cfg.child is ChildConfig()
    assert cfg.to_dict() == {"child": {"value": 1}}
