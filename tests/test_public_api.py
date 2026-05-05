from liblaf import conf
from liblaf.conf import converters


def test_conf_public_exports_match_stubbed_api() -> None:
    assert set(conf.__all__) == {
        "BaseConfig",
        "ConfigMeta",
        "Converter",
        "Factory",
        "Field",
        "Group",
        "Var",
        "__commit_id__",
        "__version__",
        "__version_tuple__",
        "field",
        "field_bool",
        "field_date",
        "field_datetime",
        "field_decimal",
        "field_float",
        "field_int",
        "field_json",
        "field_list_str",
        "field_path",
        "field_str",
        "field_time",
        "field_timedelta",
        "group",
    }
    assert conf.BaseConfig.__name__ == "BaseConfig"
    assert conf.field(default="value").default == "value"


def test_converters_public_exports_match_stubbed_api() -> None:
    assert set(converters.__all__) == {
        "identity",
        "pydantic_model_validate",
        "pydantic_model_validate_json",
        "pydantic_model_validate_strings",
        "pydantic_type_adapter_validate_json",
        "pydantic_type_adapter_validate_python",
        "pydantic_type_adapter_validate_strings",
    }
    assert converters.identity("value") == "value"
