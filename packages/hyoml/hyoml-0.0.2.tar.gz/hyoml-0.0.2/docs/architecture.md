# 🏗 Hyoml Architecture

Hyoml is built to parse, validate, manipulate, and format relaxed JSON/YAML-like data structures efficiently.

## 📦 Main Components

| Component | Description |
|:----------|:------------|
| **Parser** | Reads relaxed input (Hyoml, JSON, YAML) and constructs Python structures |
| **Formatters** | Output data into formats like JSON, YAML, XML, CSV, RDF, etc. |
| **Middleware** | Apply visitors (TagVisitor, DirectiveVisitor) to parsed structures |
| **Loader** | Load data from local, cloud, or URL sources |
| **Interface** | Expose clean API (`parse`, `format`, `validate`, etc.) to users |
| **Tests** | Ensure correctness of parsing and formatting processes |
| **Examples** | Demonstrate usage and edge cases for developers |

---

# 🎨 Design Patterns Used

## 🧩 Factory Pattern
- Used in **loader_manager.py**, **formatter_manager.py**
- Dynamically instantiate the correct loader or formatter based on input type.

## 🔀 Strategy Pattern
- Used in **loader/strategies/** and **formatters/**
- Select loading strategies or formatting strategies at runtime without changing main logic.

## 👁 Visitor Pattern
- Used in **middleware/tag_visitor.py** and **directive_visitor.py**
- Traverse and manipulate parsed data structures cleanly.

---

# 🔗 Dependency Flow

```plaintext
Parser -> Middleware Visitors -> Formatters
Loaders -> Parser -> Formatters
```

All components are modular and can be replaced or extended.

---

# 🛡 Key Principles

- No external dependencies for core parsing.
- Clear, readable Python 3.8+ code.
- Test-driven design.
- Flexibility between strict and relaxed parsing modes.
