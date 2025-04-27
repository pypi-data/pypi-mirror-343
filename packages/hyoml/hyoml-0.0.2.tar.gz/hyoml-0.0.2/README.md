# 🐍 Hyoml Python Package

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

Welcome to the Python core of the Hyoml project — a smart, relaxed parser and formatter for modern data structures.

This package provides the main Hyoml engine, formatters, validators, loaders, and interfaces.

---

## 📦 Installation

Clone the repository and install locally:

```bash
pip install -e ./python
```

Or navigate into the `python/` folder and install:

```bash
cd python
pip install -e .
```

---

## 🚀 Quick Start

Parse Hyoml content with just a few lines:

```python
from python.interface.hyoml import Hyoml

h = Hyoml()
parsed = h.parse("""
name: Alice
age: 30
country: Wonderland
""")
print(parsed)
```

Format data back into JSON, YAML, or Hyoml:

```python
print(h.format(parsed, format="json"))
print(h.format(parsed, format="yaml"))
```

---

## 🏗 Folder Structure

| Folder | Purpose |
|:-------|:--------|
| `cli/` | CLI commands and entry points |
| `cloud_storage/` | Cloud storage agent loaders |
| `examples/` | Example scripts and sample data |
| `formatters/` | Output formatters (JSON, YAML, XML, etc.) |
| `interface/` | Main Hyoml interface and helpers |
| `loader/` | Flexible local and cloud data loaders |
| `middleware/` | Tag and directive visitors |
| `parser/` | Relaxed parsers for JSON, YAML, Hyoml |
| `strict_profiles/` | Profiles for enforcing strict modes |
| `tests/` | Unit tests for parsers, formatters, utils |
| `utils/` | Common utility functions (validation, formatting) |

---

## 🧪 Running Tests

To run all tests:

```bash
cd python
pytest tests/
```

Make sure you have `pytest` installed:

```bash
pip install pytest
```

---

## 🛠 Contributing

- Fork the repository
- Create a feature branch
- Write tests for your changes
- Submit a pull request 🚀

We welcome contributions to parsers, formatters, visitors, and loaders!

---

## 📄 License

MIT License — see `LICENSE` file for details.

---

Happy Parsing with Hyoml! 🎯
