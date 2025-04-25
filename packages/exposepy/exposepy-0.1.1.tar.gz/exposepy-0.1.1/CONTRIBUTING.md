# Contributing to exposepy

Thanks for considering a contribution!

## 🛠 Getting Started

Clone and install dev deps:

```bash
git clone https://github.com/El3ssar/exposepy.git
cd exposepy
pip install -e .[dev]
```

## ✅ Guidelines

- Use `pytest` for tests.
- Keep the code clean, minimal, and readable.
- Use `@expose` for any new public function.
- Update docs if public behavior changes.

## 🧪 Run Tests

```bash
hatch run test
```

## 🧾 Code Style

Use `ruff` or `black` for formatting if preferred.

---

## 🧠 Pull Request Policy

- Keep PRs focused and small.
- If adding a feature, open an issue/discussion first.
- At least **one approval** from a maintainer is required.
- We prefer clean commits over "fix typo" clutter — use `git rebase -i` if needed.

