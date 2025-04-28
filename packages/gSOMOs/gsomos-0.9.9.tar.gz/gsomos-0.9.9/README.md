<div style="text-align:center">
<img src="https://raw.githubusercontent.com/rpoteau/gSOMOs/main/somos/config/svg/pyPCBanner-C.png" alt="SOMOs" width="1000"/>
</div>

> **Versions [0.9.0] - [0.9.9] - 2024-04-27**
>
> **Changed**
>
> - logo is now gSOMOs instead of SOMOs
> - in the projection scheme (`proj.py`), there are now two criteria to identify a SOMO, namely "SOMO P2v?" (formerly SOMO?) and "SOMO dom. β MO?" (see scientific documentation)
>     - SOMOs identified according to the P^2_virtual criterion are highlighted in green
>     - SOMOs identified only on the basis of a dominant virtual beta MO are highlighted in orange (weaker criterion)
> - Scientific documentation renamed `gSOMOs.pdf`. And content updated
> - gSOMOs-v3.pdf scientific document now downloadable in `gsomos.readthedocs.io`
> - Images in README.md now point to their `https://raw.githubusercontent.com` counterpart
> - Update of `DOCUMENTATION_setup.md`, `PUBLISHING.md`
> - Link toward the Jupyter notebook with examples and a log zip file with two Gaussian logs in `DOCUMENTATION_setup.md` and in `README.md`
>
> **Added**
>
> - new analyzis scheme in `proj.py`: bases on the diagonalization of projection matrices
> - new `clean_logfile_name()` function in `io.py` (made to solve a prefix issue for X.log.gz files)
> - Short examples in the documentation
> - docstring for `projection_heatmap_from_df`
> - docstring of `show_alpha_to_homo` translated in English
> - updated *Installation* section in `README.md`
>
> **Fixed**
> 
> - minor fixes
> - wrong initialization of `visualID_Eng` at the beginning of the notebook, and tricky issues
> 

# gSOMOs

🔗 Available on [PyPI](https://pypi.org/project/gSOMOs/)

A Python library to identify and analyze Single Occupied Molecular Orbitals (SOMOs) from Gaussian 09 or Gaussian 16 `.log` files.

[![PyPI version](https://img.shields.io/pypi/v/gSOMOs.svg?color=blue)](https://pypi.org/project/gSOMOs/)
[![Documentation Status](https://readthedocs.org/projects/gsomos/badge/?version=latest)](https://gsomos.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/github/license/rpoteau/gSOMOs)](https://github.com/rpoteau/gSOMOs/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-brightgreen.svg)](https://www.python.org/downloads/)
[![Build](https://img.shields.io/badge/build-manual-lightgrey)](https://github.com/rpoteau/gSOMOs)


<hr style="height:3px; background-color:#00aaaa; border:none;" />

## 🛠️ Installation

### ⚡ Quickstart

1. Open a terminal:

- On Linux/macOS: open a Terminal (bash)

- On Windows: open PowerShell 

2. (Recommended) Set up a local virtual environment inside your project folder using [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

    ```bash
    # Create, if necessary, a project folder
    mkdir my-project-folder

    # Move to your project directory
    cd my-project-folder

    # Create the virtual environment
    virtualenv gSOMOS-venv # or any other name that has nothing to do with gSOMOS

    # Activate the environment
    source gSOMOS-venv/bin/activate   # On Linux/macOS
    # or
    gSOMOS-venv\Scripts\activate      # On Windows
    ```

3. Install gSOMOs inside the environment:

    ```bash
    pip install gSOMOs
    ```

📦 All necessary Python packages will be installed automatically !

---

### 📋 Requirements

- 🐍 Python ≥ 3.8
- 📦 A working installation of [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- 🔄 An up-to-date version of `pip` (`python -m pip install --upgrade pip`)

---

### 📝 Notes

- Keeping the virtual environment inside the project folder makes it easier to manage and remove if needed.
- To deactivate the environment at any time, simply type:

    ```bash
    deactivate
    ```


<hr style="height:3px; background-color:#00aaaa; border:none;" />

## 🔎 Capabilities Overview

`SOMOs` is a Python toolkit for analyzing **molecular orbitals** (MOs) from Gaussian log files, with a focus on identifying **SOMOs** (Singly Occupied Molecular Orbitals) in open-shell systems.

---

### 🚀 Main Features

```python
from somos import io # optional
from somos import cosim, proj
```

#### Load Gaussian Log Files
- Parses `.log` and `.log.gz` Gaussian output files
- Extracts orbital energies, coefficients, overlap matrices, and spin

#### Cosine Similarity & SOMO Detection
- Computes cosine similarities between alpha and beta orbitals
- Identifies SOMO candidates from orbital projections

#### Projection-Based Analysis
- Projects occupied and virtual alpha MOs onto virtual beta MOs
- Decomposes projection matrix to extract leading contributions

---

### 📊 Visualization Tools

#### Heatmaps
- Interactive or static heatmaps of MO similarities

<div style="text-align: center;">
  <img src="https://raw.githubusercontent.com/rpoteau/gSOMOs/main/doc-latex/H2CO_T1_projection_heatmap-C.png" alt="heatmap" width="600px">
</div>

#### t-SNE (Dimensionality Reduction)
- Projects high-dimensional orbital space to 2D for visual exploration
- Enables inspection of orbital families and similarity patterns

<div style="text-align: center;">
  <img src="https://raw.githubusercontent.com/rpoteau/gSOMOs/main/doc-latex/H2CO_T1_tSNE-C.png" alt="tSNE" width="600px">
</div>

---

### 📁 Output
- `.xlsx` tables of SOMO similarity and projections
- `.png` images of heatmaps and projections
- All results saved in the `logs/` folder
- well-organized dataframes and printing

```
=== Summary of SOMO candidates ===

──────────── SOMO Candidate #1 ────────────
  α occupied contributions:
    • α 187 (44.2%)
    • α 164 (27.3%)
  β virtual projections:
    • β 194 (73.3%)
    • β 196 (16.1%)

──────────── SOMO Candidate #2 ────────────
  α occupied contributions:
    • α 169 (41.1%)
    • α 186 (21.6%)
    • α 165 (15.7%)
  β virtual projections:
    • β 192 (53.1%)
    • β 193 (26.9%)

──────────── SOMO Candidate #3 ────────────
  α occupied contributions:
    • α 186 (30.0%)
  β virtual projections:
    • β 198 (73.0%)

──────────── SOMO Candidate #4 ────────────
  α occupied contributions:
    • α 168 (51.8%)
    • α 183 (16.3%)
  β virtual projections:
    • β 193 (41.6%)
    • β 192 (26.7%)
```

<hr style="height:3px; background-color:#00aaaa; border:none;" />

## Examples and Documentation

### ✅ Examples Used in Notebooks (compressed Gaussian files)
- `logs/H2CO_T1.log.gz`
- `logs/FeComplex.log.gz`

---

### 📓 Example Jupyter Notebook

An example notebook demonstrating gSOMOs usage is available: [gSOMOs Examples Notebook on GitHub](https://github.com/rpoteau/gSOMOs/blob/main/SOMOs-examples.ipynb)  

Also download the [logs/ folder](https://github.com/rpoteau/gSOMOs/blob/main/logs.zip) with the two examples.

---

### 📚 Technical and scientific documentation

This [document](https://github.com/rpoteau/gSOMOs/blob/main/doc-latex/gSOMOS-v3.pdf) describes two complementary methods to identify singly occupied molecular orbitals (SOMOs) in open-shell systems:
- **Orbital projection analysis**, where occupied α orbitals are projected onto the β orbital basis using the AO overlap matrix;
- **Cosine similarity mapping**, which computes the angular similarity between α and β orbitals and matches them using the Kuhn–Munkres (Hungarian) algorithm.

The two examples, which involve finding the SOMOs of the lowest triplet state (*T*<sub>1</sub>) of formaldehyde (H<sub>2</sub>CO) and the lowest quintet state of an iron complex, are discussed in this document.

<hr style="height:3px; background-color:#00aaaa; border:none;" />

