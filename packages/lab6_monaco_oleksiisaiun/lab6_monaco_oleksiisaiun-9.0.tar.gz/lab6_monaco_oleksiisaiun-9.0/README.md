# Python_Lab_6_OOP_monaco_report

This is a Python application that implements the Monaco Racing Report in an object-oriented (OOP) format.

---

## 1. Installation

Using `uv`:

```bash
uv pip install oleksiisaiun_lab6_monaco
```

Using `pip`:

```bash
pip3 install lab6_monaco_oleksiisaiun
```

---

## 2. Examples

### 2.1. Run from a Python script:

```python
from lab6_monaco_oleksiisaiun.race_report import main_run

main_run()
```

### 2.2. Run from CLI:

```bash
python3 -c "from lab6_monaco_oleksiisaiun.race_report import main_run; main_run()"
```

---

## 3. How to publish the package to PyPI using `uv`

### 3.1. Go to the root folder of this package

```bash
cd /path/to/your/package
```

### 3.2. Run the following commands:

```bash
uv build
uv publish --token [YOUR_PYPI_TOKEN]
```
