# 🧪 How to Build the HTML Documentation for SOMOs (with Sphinx)

This guide explains how to build a full HTML documentation for the SOMOs package using **Sphinx**.

---

## ✅ 1. Install Required Packages

```bash
pip install sphinx furo
```

Optional:
```bash
pip install sphinx-autodoc-typehints
```

---

## 🛠️ 2. Initialize the Sphinx project

```bash
sphinx-quickstart docs
```

Answer:
- Separate source and build dirs → yes
- Project name → SOMOs
- Author name → Romuald Poteau
- Use Makefile → yes

---

## ✏️ 3. Edit `docs/source/conf.py`

Make sure it includes:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

html_theme = 'furo'
```

---

## 🧱 4. Edit `docs/source/index.rst`

```rst
Welcome to SOMOs's documentation!
=================================

.. automodule:: somos.io
   :members:
   :undoc-members:

.. automodule:: somos.cosim
   :members:
   :undoc-members:

.. automodule:: somos.proj
   :members:
   :undoc-members:
```

---

## 🚀 5. Build the documentation

From the `docs/` directory:

```bash
make html
```

Open the generated file:

```
docs/build/html/index.html
```

That's your full HTML documentation!

