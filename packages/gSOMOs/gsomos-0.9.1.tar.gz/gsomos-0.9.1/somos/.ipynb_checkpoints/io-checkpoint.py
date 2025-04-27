from somos.config import tools4pyPC as t4p
import os
from pathlib import Path
import re

from IPython.display import display, Markdown

import numpy as np
import pandas as pd

import cclib
from cclib.parser.utils import PeriodicTable

# ### log MOs and basic functions

def extract_gaussian_info(logfile_path):
    """
    Extracts molecular orbital and structural information from a Gaussian log file using cclib.

    Parameters
    ----------
    logfile_path : str
        Path to the Gaussian .log file.

    Returns
    -------
    dict
        A dictionary containing UDFT/DFT type, basis size, molecular orbitals, geometry,
        occupation, HOMO index, spin values, and the AO overlap matrix.
    """
    import gzip
    import shutil
    import tempfile
    from tqdm import tqdm
    
    logfile_path = Path(logfile_path)
    is_gzipped = logfile_path.suffix == ".gz"
    temp_file_path = None

    if is_gzipped:
        print(f"Need to gunzip the log file")
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log", encoding="utf-8") as temp_file:
            with gzip.open(logfile_path, "rt", encoding="utf-8") as f_in:
                # Get the total uncompressed size if possible
                total_size = 0
                try:
                    with gzip.open(logfile_path, "rb") as f_check:
                        f_check.read()
                        total_size = f_check.tell()
                except Exception:
                    pass  # ignore if we can't estimate
    
                # Now gunzip with a progress bar
                chunk_size = 1024 * 1024  # 1 MB
                with tqdm(total=total_size, unit="B", unit_scale=True, desc="Gunzip") as pbar:
                    while True:
                        chunk = f_in.read(chunk_size)
                        if not chunk:
                            break
                        temp_file.write(chunk)
                        pbar.update(len(chunk))
            temp_file_path = temp_file.name
        logfile_path = Path(temp_file_path)

    if not logfile_path.is_file():
        raise FileNotFoundError(f"File not found: {logfile_path}")

    data = cclib.io.ccread(str(logfile_path))

    # Parse <S**2> line BEFORE deleting the temp file
    S2_val = None
    S_val = None
    multiplicity = None
    try:
        with open(logfile_path, "r") as f:
            lines = f.readlines()
        for line in reversed(lines):
            if "<S**2>" in line and "S=" in line:
                match = re.search(r"<S\*\*2>=\s*([\d.]+)\s+S=\s*([\d.]+)", line)
                if match:
                    S2_val = float(match.group(1))
                    S_val = float(match.group(2))
                    multiplicity = round(2 * S_val + 1, 1)
                    print(f"Eigenvalue of S2 operator = {S2_val}") 
                    print(f"S-value = {S_val}") 
                    print(f"Spin multiplicity = {multiplicity}") 
                    expected_nMag = 2 * S_val
                    print(f"2×S = {expected_nMag:.2f} → expecting ~{round(expected_nMag)} magnetic orbitals (SOMOs)")
                break
    except Exception:
        pass
    
    # Now cleanup
    if is_gzipped and temp_file_path:
        os.remove(temp_file_path)
    
    nbasis = getattr(data, "nbasis", None)
    if nbasis is None:
        raise ValueError("🛑 `nbasis` is missing. Cannot proceed without the number of basis functions.")

    final_geom = data.atomcoords[-1] if hasattr(data, "atomcoords") else []
    atomic_numbers = getattr(data, "atomnos", [])
    pt = PeriodicTable()
    optimized_geometry = [
        {
            "Z": int(Z),
            "symbol": pt.element[Z],
            "x": float(x),
            "y": float(y),
            "z": float(z)
        }
        for Z, (x, y, z) in zip(atomic_numbers, final_geom)
    ]

    MO_coeffs = data.mocoeffs if hasattr(data, "mocoeffs") else None

    if hasattr(data, "moenergies"):
        MO_energies = [e / 27.21139 for e in data.moenergies]
    else:
        MO_energies = None

    MO_occ = None
    homo_index = None
    DFT_type = None

    if hasattr(data, "homos") and MO_energies:
        homos = data.homos
        n = len(data.moenergies[0])
        if np.ndim(homos) == 1 and len(homos) == 2:
            DFT_type = "UDFT"
            MO_occ = []
            for homo in homos:
                occ = ["O" if i <= homo else "V" for i in range(n)]
                MO_occ.append(occ)
            homo_index = list(homos)
        else:
            DFT_type = "DFT"
            homo = int(homos.item())
            MO_occ = ["O" if i <= homo else "V" for i in range(n)]
            homo_index = homo


    overlap_matrix = getattr(data, "aooverlaps", None)
    if overlap_matrix is None:
        print("⚠️ WARNING: AO overlap matrix not found. Using identity matrix instead.")
        print()
        overlap_matrix = np.identity(nbasis)

    return {
        "UDFT_or_DFT": DFT_type,
        "nbasis": nbasis,
        "n_MO": len(MO_energies[0]) if MO_energies else None,
        "MO_coeffs": MO_coeffs,
        "MO_energies": MO_energies,
        "MO_occ": MO_occ,
        "HOMO_index": homo_index,
        "optimized_geometry": optimized_geometry,
        "overlap_matrix": overlap_matrix,
        "spin": {
            "S2": S2_val,
            "S": S_val,
            "multiplicity": multiplicity
        }
    }

def load_mos_from_cclib(logfolder, filename):
    """
    Loads molecular orbital data from Gaussian output using cclib and organizes them into DataFrames.

    Parameters
    ----------
    logfolder : str or Path
        Directory containing the log file.
    filename : str
        Name of the Gaussian .log file.

    Returns
    -------
    tuple
        Alpha and beta DataFrames, coefficient matrices, basis count, overlap matrix, and full info dictionary.
    """
    
    logfile_path = Path(logfolder) / filename
    info = extract_gaussian_info(logfile_path)
    t4p.centerTitle("🚨 ENTERING load_mos_from_cclib 🚨")

    coeffs = info["MO_coeffs"]
    energies = info["MO_energies"]
    occupations = info["MO_occ"]
    nbasis = info["nbasis"]
    overlap_matrix = info["overlap_matrix"]

    if info["UDFT_or_DFT"] == "UDFT":
        print("UDFT")
        alpha_df = pd.DataFrame({
            "Index": np.arange(1, len(occupations[0]) + 1),
            "Occupation": occupations[0],
            "Energy (Ha)": energies[0]
        })
        beta_df = pd.DataFrame({
            "Index": np.arange(1, len(occupations[1]) + 1),
            "Occupation": occupations[1],
            "Energy (Ha)": energies[1]
        })
        print("✅ Finished load_mos_from_cclib")
        return alpha_df, beta_df, coeffs[0], coeffs[1], nbasis, overlap_matrix, info
    else:
        print("DFT")
        alpha_df = pd.DataFrame({
            "Index": np.arange(1, len(occupations) + 1),
            "Occupation": occupations,
            "Energy (Ha)": energies[0]
        })
        print("✅ Finished load_mos_from_cclib")
        return alpha_df, alpha_df, coeffs[0], coeffs[0], nbasis, overlap_matrix, info

def clean_logfile_name(logfile):
    """
    Given a log file name (e.g., 'myfile.log' or 'myfile.log.gz'),
    returns the base calculation name without any '.log' or '.log.gz' extension.

    Parameters
    ----------
    logfile : str or Path
        The name of the Gaussian log file.

    Returns
    -------
    str
        The cleaned calculation name, without the '.log' or '.log.gz' suffix.
    """
    name = Path(logfile).stem
    if name.endswith(".log"):
        name = name[:-4]
    return name
