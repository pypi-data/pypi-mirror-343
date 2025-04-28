# 🧮 Main Commands for Using gSOMOs

<div style="text-align: center;">
  <img src="_static/pyPCBanner.svg" alt="gSOMOs Banner" width="800px">
</div>
<br>

This page summarizes the essential commands you need to use gSOMOs, along with a short explanation for each.
Working examples are vailable in a [gSOMOs Examples Jupyter Notebook on GitHub](https://github.com/rpoteau/gSOMOs/blob/main/SOMOs-examples.ipynb)

---

## 📂 Load Gaussian Log Files

```python
from somos import io

alpha_df, beta_df, alpha_mat, beta_mat, nbasis, overlap_matrix, info = io.load_mos_from_cclib(logfolder, logfile)
```
→ Loads alpha and beta molecular orbitals, coefficients, overlap matrix, and other information from a Gaussian log file. It is usually done internally. Whatever the way you decide to load a G09 or G16 log file - that can be gzipped to save disk space - dont forget to initialize `logfolder` (eg `logfolder = "./logs"`) and `logfile` (eg `logfile` = "H2CO.log.gz")

---

## 📈 Analyze Cosine Similarity Between Orbitals

### Main routine

```python
from somos import cosim

listMOs, coeffMOs, nBasis, dfSOMOs, S = cosim.analyzeSi milarity(logfolder, logfile)

cosim.save_similarity_per_somo_from_df(dfSOMOs, listMOs, coeffMOs, nBasis, S, logfolder, logfile)
```
→ Calculates cosine similarities between alpha and beta orbitals to identify SOMO candidates. Saves results to Excel files.

### Heatmap

```python
cosim.heatmap_MOs(listMOs, coeffMOs, nBasis, S, logfolder, logfile)
```
→ Interactive cosine similarity heatmap between alpha and beta MOs around the HOMO-LUMO frontier

### tSNE analyzis and plot

```python
cosim.tsne(listMOs, coeffMOs, S, logfolder,logfile)
```
→ Performs a t-SNE projection of molecular orbitals (alpha and beta) using a cosine similarity
metric invariant to phase, and displays an interactive Plotly visualization

---

## 📊 Projection Analysis

### Main routine

```python
from somos import proj

df_proj, info = proj.project_occupied_alpha_onto_beta(logfolder, logfile)
proj.projection_heatmap_from_df(df_proj, logfolder, logfile)
```
→ Projects occupied alpha orbitals onto virtual beta orbitals and generates a heatmap of the projection matrix.

### Heatmap

```python
proj.projection_heatmap_from_df(df_proj, info["nbasis"], logfolder, logfile)
```
→ Generates an interactive heatmap visualization of the main projections
    between occupied/virtual alpha and beta molecular orbitals (MOs) from a Gaussian log file

### Projection of the occupied alpha MOs on the space spanned by the beta occupied MOs

```python
from somos import proj

proj.diagonalize_alpha_occ_to_beta_occ_and_virt_separately(logfolder,logfile)
```
→ Projects occupied alpha orbitals separately onto beta occupied and beta virtual subspaces,
diagonalizes the two projection matrices, and analyzes dominant contributions
