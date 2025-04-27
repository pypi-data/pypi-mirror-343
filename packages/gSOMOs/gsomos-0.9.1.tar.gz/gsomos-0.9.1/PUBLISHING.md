# 📦 Publishing SOMOs on PyPI

This memo summarizes all the steps to build and publish the `SOMOs` package.

---

## 🔧 Setup (one-time)

activate your python environment, if relevant

```bash
pip install build twine
```

---

## 🧑‍💻 Create a PyPI or TestPyPI account

If you haven’t already, create an account on:

- [TestPyPI](https://test.pypi.org/account/register/)
- [Real PyPI](https://pypi.org/account/register/)

Then log in.

------------

## 🪪 Create a PyPI or TestPyPI API token

To avoid using your real password when uploading, create a secure API token:

- Go to your **Account Settings → API tokens**
- Click **"Add API token"**
- Choose a name and a scope (entire account or a specific project)
- Copy the generated token (it starts with `pypi-...`) — you’ll only see it once!

Links:
- [TestPyPI token management](https://test.pypi.org/manage/account/#api-tokens)
- [PyPI token management](https://pypi.org/manage/account/#api-tokens)

---

## 🔐 Optional: Save your token in a `.pypirc` file

Create a file named `.pypirc` in your home directory (`~/.pypirc`):

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXX

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

This avoids typing the token every time you use `twine upload`.

---

## 🏗️ Build the package

Run from the project root (where `pyproject.toml` is):

```bash
rm -rf dist/ build/ SOMOs.egg-info/ # unless it is the first time you try to build the package
python -m build
```

This creates a `dist/` folder with:
- `somos-x.y.z.tar.gz` (source)
- `somos-x.y.z-py3-none-any.whl` (wheel)

Don't forget to update the version number in `pyproject.toml`

---

## 📤 Upload to TestPyPI (sandbox)

```bash
twine upload --repository testpypi dist/*
```

Then install from TestPyPI to test:

```bash
pip install -i https://test.pypi.org/simple SOMOs
```

---

## 📤 Upload to real PyPI

Once you're confident with TestPyPI:

```bash
twine upload dist/*
```

---

## 🧼 Clean up build files (recommended)

```bash
rm -rf build dist SOMOs.egg-info
```

---


## ✅ Install your package locally (editable mode)

```bash
pip install -e .
```

Then in Python:

```python
from somos import io, cosim, proj
```

---


## 🚀 Fast process

```bash
rm -rf build dist SOMOs.egg-info
python -m build
twine upload dist/*
pip install -e .
```

<hr style="height:3px; background-color:#00aaaa; border:none;" />


# 🧠 What is `pip install -e .` (Editable Install)?

This part explains **what `pip install -e .` does**, why it’s useful, and how it applies to your project `SOMOs`.

---

## 📦 What does it do?

```bash
pip install -e .
```

means:

> "Tell Python to install this package **in editable mode** — don’t copy the code, just link to it so any changes I make to the source code take effect immediately."

This is also called **"develop mode"** or **"symlink install"**.

---

## 🗂️ Folder structure required

You must run the command in the folder where your `pyproject.toml` is located, and this file must define the name of your package:

```
~/projects/SOMOS-4pyPi/
├── pyproject.toml              👈 defines `project.name = "SOMOs"`
├── somos/                      👈 your actual package code
│   ├── __init__.py
│   ├── io.py
│   ├── cosim.py
│   └── proj.py
```

---

## ✅ What happens when you run it

In your terminal:

```bash
cd ~/projects/SOMOS-4pyPi
pip install -e .
```

Python:
- Reads `pyproject.toml`
- Sees `name = "SOMOs"`
- Registers a **symlink** to `somos/` in your Python environment
- So when you do `from somos import io`, it looks in this folder

You should see:

```
Successfully built SOMOs
Successfully installed SOMOs
```

If you see:

```
Found existing installation: SOMOs x.y.z
Can't uninstall 'SOMOs'. No files were found to uninstall.
```

That’s just a harmless notice: it means the package was previously installed in editable mode and there’s nothing to uninstall. Your new editable install **still works**.

---

## 🧪 Why is this useful?

Because if you edit any `.py` file (e.g. `cosim.py`), you don’t need to reinstall your package — the changes take effect immediately.

Perfect for development, notebooks, or live testing.

---

## ⚠️ Does it overwrite anything?

**No. Nothing is copied or erased.**  
It just tells your Python environment:

> "If someone does `import somos`, use this exact local folder right here."

---

## 🗺️ Where does it install?

To see what it actually does, run:

```bash
pip show SOMOs
```

This will show you the linked path and confirm it's using your local files.

---

## ✅ Example usage in notebook

Once installed:

```python
from somos import io, cosim, proj
```

Now modify any file in `somos/`, save it, and your notebook will reflect the change immediately!

