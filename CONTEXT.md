# liblaf.conf

`liblaf.conf` describes application settings that can be read consistently in
normal code and temporarily varied in one execution context.

## Language

**Field**:
A declared named setting that binds to one context-local variable on a config.
_Avoid_: Property, option

**Active value**:
The value a field resolves in the current execution context.
_Avoid_: Global value, process value

**Declared default**:
The field value or factory result used when no active value or environment
value is present.
_Avoid_: Fallback, cached value
