# Value resolution

Reading a variable follows a fixed order in the active context: an explicitly
stored value first, then a fresh factory result, then a deep copy of the
declared default. A variable without any value raises `LookupError` unless
`get(default)` supplies a call-site fallback.

Every source passes through the field converter: environment strings,
`set()`/`override()` values, declared defaults, and factory results. A converter
failure is therefore visible at the operation that introduced the value rather
than deferred to a later consumer.

Declared defaults are copied when materialized, so mutating a default list in
one context does not mutate the source default or another context's fresh
value. This copying rule does not apply to values manually installed with
`set()`.
