# Nested configs and serialization

Use `group(ChildConfig)` to compose settings. `load_env()`, `set()`, and
`override()` recurse into nested mappings, so callers can update a tree without
handling its bound `Var` objects individually.

`to_dict()` builds fresh dictionaries for the tree and `to_namespace()` builds
fresh namespaces. Their leaves are the current field values themselves, not
deep copies. Treat their result as a convenient structural view, not an
immutable snapshot; copy mutable leaves before handing them to code that may
retain or mutate them.
