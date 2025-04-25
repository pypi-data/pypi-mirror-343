# exposepy

[![PyPI](https://img.shields.io/pypi/v/exposepy.svg)](https://pypi.org/project/exposepy/)
[![CI](https://github.com/El3ssar/exposepy/actions/workflows/ci.yml/badge.svg)](https://github.com/El3ssar/exposepy/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-online-brightgreen.svg)](https://El3ssar.github.io/exposepy/)

Minimalist decorator for exposing public APIs in Python.

---

## 💡 What is this?

`exposepy` lets you declaratively define your public API using `@expose` and `reexpose()`.  
No more manual `__all__`, no more forgotten exports. Refactor-proof and clean.

---

## 🚀 Installation

```bash
pip install exposepy
```

---

## 🛠️ Basic Usage

```python
from exposepy import expose

@expose
def foo():
    return 42

@expose(name="bar_alias")
def bar():
    return "bar"
```

Your module’s `__all__` and `dir()` now only show `foo` and `bar_alias`.

---

## 🔁 Cross-module Re-Export

```python
from module_a import foo
from exposepy import reexpose

reexpose(foo)  # Now foo is part of module_b.__all__
```

---

## 🧠 Why Use exposepy?

- Refactor-proof exports
- Auto-maintained `__all__`
- Cleaner introspection via patched `__dir__`
- Declarative, not imperative
- Cross-module reexports with aliasing

---

## 📚 Documentation

→ [https://El3ssar.github.io/exposepy](https://El3ssar.github.io/exposepy)

---

## 🤝 Contributing

Contributions welcome!  
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and how to get started.
