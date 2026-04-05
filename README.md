<div align="center" markdown>

![conf](https://socialify.git.ci/liblaf/conf/image?description=1&forks=1&issues=1&language=1&name=1&owner=1&pattern=Transparent&pulls=1&stargazers=1&theme=Auto)

**[Explore the docs »](https://liblaf.github.io/conf/)**

[![PyPI - Version](https://img.shields.io/pypi/v/liblaf-conf?logo=PyPI)](https://pypi.org/project/liblaf-conf/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/liblaf-conf?logo=Python)](https://pypi.org/project/liblaf-conf/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/liblaf-conf?logo=PyPI)](https://pypi.org/project/liblaf-conf/)
[![Python / Test](https://github.com/liblaf/conf/actions/workflows/python-test.yaml/badge.svg)](https://github.com/liblaf/conf/actions/workflows/python-test.yaml)
[![Python / Docs](https://github.com/liblaf/conf/actions/workflows/python-docs.yaml/badge.svg)](https://github.com/liblaf/conf/actions/workflows/python-docs.yaml)
[![Codecov](https://codecov.io/gh/liblaf/conf/graph/badge.svg)](https://codecov.io/gh/liblaf/conf)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[Changelog](https://github.com/liblaf/conf/blob/main/CHANGELOG.md) · [Report Bug](https://github.com/liblaf/conf/issues) · [Request Feature](https://github.com/liblaf/conf/issues)

![Rule](https://cdn.jsdelivr.net/gh/andreasbm/readme/assets/lines/rainbow.png)

</div>

Typed configuration primitives for Python applications built on descriptors,
`contextvars`, and environment-aware converters.

## ✨ Features

- 🧩 **Declarative config objects:** Define settings once with `BaseConfig`,
  `Field`, and `group()` instead of wiring ad hoc globals or dictionaries.
- 🌱 **Environment-aware loading:** Bind fields to derived or explicit
  environment variable names and refresh them with `load_env()`.
- 🎯 **Typed conversion helpers:** Use built-in `field_*` helpers for booleans,
  numbers, JSON, paths, and temporal values.
- 🔄 **Scoped overrides:** Temporarily swap values with `Var.override()` or
  `BaseConfig.override()` while preserving `contextvars` semantics.
- 🪺 **Nested config trees:** Compose related settings into groups and serialize
  them with `to_dict()` or `to_namespace()`.

## 📦 Installation

> [!NOTE]
> `liblaf-conf` supports Python 3.12 and newer.

```bash
uv add liblaf-conf
```

## 🚀 Quick Start

```python
from liblaf import conf


class DatabaseConfig(conf.BaseConfig):
    url: conf.Field[str] = conf.Field(default="sqlite:///app.db")


class AppConfig(conf.BaseConfig):
    debug: conf.Field[bool] = conf.field_bool()
    database: conf.Group[DatabaseConfig] = conf.group(DatabaseConfig)


cfg = AppConfig()

cfg.set(debug=True, database={"url": "sqlite:///dev.db"})

with cfg.override(debug=False):
    assert cfg.debug.get() is False

assert cfg.to_dict() == {
    "debug": True,
    "database": {"url": "sqlite:///dev.db"},
}
```

`BaseConfig` subclasses are singletons, so calling `AppConfig()` again returns
the same config object.

## ⌨️ Local Development

Clone the repository and use the maintained task surfaces:

```bash
git clone https://github.com/liblaf/conf.git
cd conf
mise install
mise run lint
nox --tags test
mise run docs:serve
```

`mise` provides the primary setup, lint, and docs commands in this repository.
`nox` drives the test matrix used by CI.

## 🤝 Contributing

Issues and pull requests are welcome, especially when they improve the public
API, docs, or typed conversion helpers.

[![PR WELCOME](https://img.shields.io/badge/%F0%9F%A4%AF%20PR%20WELCOME-%E2%86%92-ffcb47?labelColor=black&style=for-the-badge)](https://github.com/liblaf/conf/pulls)

[![Contributors](https://gh-contributors-gamma.vercel.app/api?repo=liblaf/conf)](https://github.com/liblaf/conf/graphs/contributors)

## 🔗 Links

- [Documentation](https://liblaf.github.io/conf/)
- [PyPI](https://pypi.org/project/liblaf-conf/)
- [Source Code](https://github.com/liblaf/conf)
- [Release Notes](https://github.com/liblaf/conf/releases)

---

#### 📝 License

Copyright © 2026 [liblaf](https://github.com/liblaf). <br />
This project is [MIT](https://github.com/liblaf/conf/blob/main/LICENSE)
licensed.
