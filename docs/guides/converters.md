# Converters

Use the `field_*` helpers when their conversion rule matches the setting:
`field_bool`, `field_int`, `field_float`, `field_decimal`, `field_json`,
`field_list_str`, `field_path`, and date/time helpers cover the usual cases.

`field_list_str` splits and trims strings while preserving empty items. JSON
fields decode a string but leave an already-Python value unchanged. The temporal
helpers use Pydantic-backed validation. For application-specific values, pass a
converter directly to `field()` or `Field`; it receives both environment
strings and direct Python assignments.
