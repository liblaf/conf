# Var owns value normalization

Environment loading, direct assignment, and scoped overrides all pass through a field's converter in `Var`. Keeping that rule behind the existing `Var` interface makes typed configuration consistent without adding another validation surface.
