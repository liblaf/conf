# Reload clears absent environment values

For the active context, `load_env()` installs a present environment value and clears an absent one so resolution returns to a fresh declared default. Retaining a stale prior value would make repeated reloads depend on history rather than current environment state.
