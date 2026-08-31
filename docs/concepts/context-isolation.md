# Context isolation

`Var` stores its active value in `contextvars.ContextVar`. An override therefore
belongs to the current execution context, not to the config singleton itself.
Nested overrides unwind in reverse order even when the block raises.

New async tasks inherit the context that exists when they are created. Later
changes do not retroactively update existing tasks, and threads have separate
contexts. This makes a cached `BaseConfig` suitable for request-, test-, or
operation-local settings as long as callers do not share mutable values by
manually setting the same object.
