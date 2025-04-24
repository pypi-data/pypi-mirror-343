# py-shipstation

An unofficial [ShipStation API](https://www.shipstation.com/docs/api/) Python Client

[https://pypi.org/project/pyshipstation/](https://pypi.org/project/pyshipstation/)

Install

```bash
pip install pyshipstation
```

# Publishing to PyPi

```bash
python -m build
```

```bash
python -m twine upload --repository pypi dist/*
```

# Code Quality

Formatting
```bash
ruff format .
```

# Tests

Run the test suite
```bash
pytest tests/
```
