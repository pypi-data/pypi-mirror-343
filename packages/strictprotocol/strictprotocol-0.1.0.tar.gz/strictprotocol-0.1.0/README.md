# StrictProtocol

**StrictProtocol** is a lightweight runtime validation layer for Python's `Protocol`, enforcing exact method signature conformance at class definition time.

## 🔍 Features

- Enforces **method existence** and **signature compliance** for protocol implementations
- Catches missing or mismatched methods early—at class creation
- Drop-in compatible with `typing.Protocol`

## 🚀 Example

```python
from typing import Protocol
from strictprotocol import StrictProtocol

class Greeter(Protocol):
    def greet(self, name: str) -> str: ...

class MyGreeter(StrictProtocol, Greeter):
    def greet(self, name: str) -> str:
        return f"Hello, {name}"
```

## 📦 Installation

```bash
pip install strictprotocol
```

## 📖 Documentation

Coming soon at [https://github.com/YOUR_USERNAME/strictprotocol](https://github.com/YOUR_USERNAME/strictprotocol)

## 🧪 Testing

To run tests:

```bash
pytest tests/
```

## 📄 License

MIT
