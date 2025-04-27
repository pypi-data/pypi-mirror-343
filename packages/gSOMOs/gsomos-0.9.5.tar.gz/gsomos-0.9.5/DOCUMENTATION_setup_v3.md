# 🧪 How to Build and Publish the HTML Documentation for gSOMOs (with Sphinx + ReadTheDocs)

This guide explains how to build and publish full HTML documentation for the gSOMOs package using **Sphinx** and **ReadTheDocs**.

---

## ✅ 1. Install Required Packages

```bash
pip install sphinx sphinx_rtd_theme myst-parser numpydoc
```

Optional:
```bash
pip install sphinx-autodoc-typehints
```

---

## 🛠️ 2. Initialize the Sphinx Project (only needed once)

```bash
sphinx-quickstart docs
```

Answer:
- Separate source and build dirs → yes
- Project name → gSOMOs
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
    'sphinx.ext.githubpages',
    'myst_parser',
    'numpydoc',
]

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
html_extra_path = ['_static']
```

---

## 🛠️ Explanation: `html_static_path` vs `html_extra_path`

- `html_static_path = ['_static']`
  - ➔ Tells Sphinx where to find **static assets** like CSS files, JS files, and local images used for theming or layout.
- `html_extra_path = ['_static']`
  - ➔ Tells Sphinx to **copy raw files (PDFs, datasets, etc.)** into the final built HTML folder, so they are downloadable.

✅ You can safely use both for `_static/` if you want to include custom styles **and** downloadable files like `.pdf`.

---

## 🧱 4. Edit `docs/source/index.rst`

```rst
Welcome to gSOMOs's documentation!
===================================

.. image:: _static/pyPCBanner.svg
   :alt: gSOMOs Banner
   :align: center
   :width: 800px

.. automodule:: somos.io
   :members:
   :undoc-members:

.. automodule:: somos.cosim
   :members:
   :undoc-members:

.. automodule:: somos.proj
   :members:
   :undoc-members:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   SOMOs_SciDoc.md
   SOMOs_examples.md
   SOMOs_dependencies.md
```

✅ This structure:
- Displays a large banner at the top.
- Auto-documents all modules.
- Organizes extra pages (scientific background, examples, dependencies).

---

## 🚀 5. Build the Documentation Locally

From the `docs/` directory:

```bash
make html
```

Then open:

```
docs/build/html/index.html
```

✅ You can check your site locally before publishing.

---

## 🌍 6. Publish on ReadTheDocs

### 🔹 Step 1: Create an Account on ReadTheDocs

- Go to [https://readthedocs.org/](https://readthedocs.org/)
- Sign up (you can use your GitHub account directly).

### 🔹 Step 2: Connect Your GitHub Repository

- Import a project.
- Authorize ReadTheDocs to access your GitHub repositories.
- Select `gSOMOs` from your repositories list.

### 🔹 Step 3: Configure the Build

- Branch: `main`
- Documentation path: `docs/`
- Configuration file: `docs/source/conf.py`

✅ RTD will detect your `readthedocs.yml` (if any) or default settings.

### 🔹 Step 4: Trigger First Build

- Save the configuration.
- ReadTheDocs will fetch your GitHub project, install dependencies, build HTML, and publish it.

✅ Your doc will be available at:
```
https://gsomos.readthedocs.io/
```

---

# ✅ You are done!

You now have:
- A locally buildable documentation (`make html`)
- A publicly accessible website (`https://gsomos.readthedocs.io/`)
- Automatic rebuild on every GitHub push 🚀

---
