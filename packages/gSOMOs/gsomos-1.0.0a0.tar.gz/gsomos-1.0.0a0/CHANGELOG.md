# 📜 Changelog

All notable changes to this gSOMOs project will be documented here.

---

## [1.0.0a] - 2024-04-27
### Fixed 
- minor typos in `README.md`

---

## [0.9.9] - 2024-04-27
### Changed 
- updated *Installation* section in `README.md`

---

## [0.9.8] - 2024-04-27
### Fixed
- residual issues in `visualID_Eng.py`

---

## [0.9.7] - 2024-04-27
### Fixed
- wrong initialization of `visualID_Eng.py` at the beginning of the notebook

---

## [0.9.6] - 2024-04-27
### Changed
- Link toward the Jupyter notebook with examples and a log zip file with two Gaussian logs in `DOCUMENTATION_setup.md` and in `README.md`

---

## [0.9.5] - 2024-04-27
### Changed
- Update of `DOCUMENTATION_setup.md` and of `PUBLISHING.md`

---

## [0.9.4] - 2024-04-26
### Changed
- Images in README.md now point to their `https://raw.githubusercontent.com` counterpart

---

## [0.9.3] - 2024-04-26
### Fixed
- Minor fixes

---

## [0.9.2] - 2024-04-26
### Added
- short examples in the documentation
- docstring for `projection_heatmap_from_df`
- docstring of `show_alpha_to_homo` translated in English

---

## [0.9.1] - 2024-04-26
### Changed
- gSOMOs-v3.pdf scientific document now downloadable in `gsomos.readthedocs.io`

---

## [0.9.0] - 2024-04-26
### Changed
- logo is now gSOMOs instead of SOMOs
- in the projection scheme (`proj.py`), there are now two criteria to identify a SOMO, namely "SOMO P2v?" (formerly SOMO?) and "SOMO dom. β MO?" (see scientific documentation)
    - SOMOs identified according to the P^2_virtual criterion are highlighted in green
    - SOMOs identified only on the basis of a dominant virtual beta MO are highlighted in orange (weaker criterion)
- Scientific documentation renamed `gSOMOs.pdf`. And content updated
### Added
- new analyzis scheme in `proj.py`: bases on the diagonalization of projection matrices
- new `clean_logfile_name()` function in `io.py` (made to solve a prefix issue for X.log.gz files)

---

## [0.2.6] - 2024-04-25
### Added
- progession bar in `io.extract_gaussian_info`
- dependency on `tqdm` added in `pyproject.toml` and to `docs/source/SOMOs_imports_summary.md`
- in `index.rst`, new calls to
    - SOMOs_imports_summary.md
    - SciDoc.md
- new `Cplx_1_OH442b_RC35_YC427_5.log.gz` example in `logs/`
### Changed
- sphinx documentation : link toward the scientific document now given in `SciDoc.md`

---

## [0.2.5] - 2024-04-25
### Changed
- documentation now available on [readthedocs](https://gsomos.readthedocs.io/)
- `pyproject.toml` changed accordingly
- `README.md` changed as well, with badges

---

## [0.2.4] - 2024-04-25
### Added
- svg files available again on github
### Changed
- docs/build/html/ now in sphinx_rtd_theme

--- 

## [0.2.3] - 2024-04-25
### Fixed
- content of docs/build/html/ is now copied in docs/

## [0.2.2] - 2024-04-25
### Added
- new [github repository](https://github.com/rpoteau/gSOMOs/)
- new link toward the documentation in pyproject.toml
- link toward doc-latex/projection-v2.pdf removed in README.md

---

## [0.2.1] - 2024-04-24
### Fixed
- added again `*.pdf` in `.gitignore`
- added `doc-latex/*.pdf` in `.gitignore`
- added MANIFEST.in

---

## [0.2.0] - 2024-04-24
### Fixed
- removed `*.pdf` in `.gitignore`

---

## [0.1.9] - 2024-04-24
### Added
- Added `CHANGELOG.md`

---

## [0.1.8] - 2024-04-24
### Added
- Official release of `gSOMOs` on [PyPI](https://pypi.org/project/gSOMOs/)
- Link toward [PyPI](https://pypi.org/project/gSOMOs/) in `README.md`

### Improved
- Finalized project name after conflict with `somos`
- Confirmed compatibility of `.log.gz` support with Gaussian files
- PyPI upload workflow and authentication instructions

### Documentation
- Added detailed publishing guide
- Added SVG banner handling in Sphinx documentation
- Structured examples and notebook summary

---

## [0.1.5] - 2024-04-24
### Added
- Automatic support for `.log.gz` compressed Gaussian files
- Added a PyPI badge to the GitHub `README.md`
- Generated Sphinx documentation scaffold with custom theming
- Markdown summaries of features and usage

### Fixed
- `<S**2>` spin parsing now runs before deleting temp files
- Improved PyPI packaging logic for `twine upload`
- Clarified error messages during `pip install -e .` behavior

---

## [0.1.4] - 2024-04-23
### Changed
- Project renamed from `SOMOs` to `gSOMOs` to avoid conflict on PyPI
- Updated all references in `README.md` and `pyproject.toml`
- Switched badge links to lowercase for compatibility with Shields.io

---

## [0.1.3] - 2024-04-22
### Added
- Initial modularization of the project into `io`, `cosim`, and `proj`
- Split functionality cleanly between loading, similarity, and projection
- Editable install and internal testing

---

## [0.1.0] - 2024-04-19
### Added
- First public version of the SOMOs utility
- Support for UDFT/DFT Gaussian logs
- Cosine similarity detection of SOMOs
- Projection-based analysis of alpha → beta orbitals
- Interactive heatmaps and 2D t-SNE projection
