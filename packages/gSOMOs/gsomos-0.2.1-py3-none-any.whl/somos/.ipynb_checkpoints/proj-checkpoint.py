from somos.config import tools4pyPC as t4p
import os
from pathlib import Path
import re

from IPython.display import display, Markdown

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# ### Projection
# 
# #### Main projection scheme


# #### heatmaps

def project_occupied_alpha_onto_beta(logfolder, logfile, threshold_beta=20):
    """
    Projects each occupied alpha orbital onto the full set of beta orbitals (occupied + virtual)
    using the AO overlap matrix. Returns a summary DataFrame including projection norms,
    dominant beta contributions, and diagnostic flags.

    Parameters
    ----------
    logfolder : str
        Path to the folder containing the Gaussian log file.
    logfile : str
        Name of the Gaussian log file.
    threshold_beta : float, optional
        Percentage threshold (default: 20) above which a beta orbital is considered significant in the projection.

    Returns
    -------
    pd.DataFrame
        DataFrame with one row per occupied alpha orbital and the following columns:
        - 'Alpha OM': Index (1-based) of the alpha orbital
        - 'Occ α': Occupation of the alpha orbital (usually 'O')
        - 'Energy (Ha)': Energy of the alpha orbital
        - 'Projection² on β_virtual': Squared norm of the projection onto the virtual beta space
        - 'Projection² on β_occupied': Squared norm of the projection onto the occupied beta space
        - 'Dominant β MO': Index (1-based) of the beta orbital with the largest projection
        - 'Index4Jmol': Jmol-compatible index for the dominant beta orbital
        - 'Occ β': Occupation of the dominant beta orbital ('V' or 'O')
        - 'E (β, Ha)': Energy of the dominant beta orbital
        - 'Top 1 contrib (%)': Percentage of the total projection norm carried by the most contributing beta orbital
        - 'Top 2 contrib (%)': Cumulative contribution of the top 2 beta orbitals
        - 'Top 3 contrib (%)': Cumulative contribution of the top 3 beta orbitals
        - 'Dominance ratio': Largest single contribution / total projection
        - 'Spread?': Flag indicating whether the projection is distributed ("Yes" if <60% dominance)
        - 'β orbitals >{threshold_beta}%': List of tuples [OM index (1-based), contribution (%)] for beta orbitals contributing >{threshold_beta value}%
        - 'SOMO?': Yes if projection is dominant onto virtual space and small on occupied

    Notes
    -----
    The squared projection of an occupied alpha orbital \( \phi^\alpha_i \) onto the full beta space is computed as:

    \[
    \mathbf{v}_i = \phi^\alpha_i \cdot S \cdot (\phi^\beta)^T
    \]

    where \( S \) is the AO overlap matrix, and \( \phi^\beta \) is the matrix of beta MOs. The squared norm \( \|\mathbf{v}_i\|^2 \) represents the total overlap.

    Top-N contributions are computed by squaring the individual projections \( v_{ij} \), sorting them, and evaluating the cumulative contributions from the top 1, 2, or 3 beta orbitals. These are returned as "Top 1 contrib (%)", "Top 2 contrib (%)", and "Top 3 contrib (%)".

    The column "β orbitals >{threshold_beta}%" lists all beta orbitals contributing more than the specified percentage to the squared projection norm, with both their index (1-based) and contribution in percent.

    The flag "SOMO?" is set to "Yes" if the squared projection on the virtual beta subspace is greater than 0.5, and the projection on the occupied beta subspace is below 0.5.

    The total number of beta orbitals \( N \) used in the projection is equal to the total number of molecular orbitals in the beta spin channel. The projection is performed over the complete beta space, regardless of occupation.
    """

    from openpyxl import Workbook
    from openpyxl.styles import PatternFill
    from openpyxl.utils.dataframe import dataframe_to_rows
    
    from .io import load_mos_from_cclib
    
    def save_projection_results_to_excel(df_sorted, logfolder, logfile):
        """
        Saves the sorted DataFrame of alpha → beta projections to an Excel file,
        highlighting the SOMO lines in light yellow.
    
        Parameters
        ----------
        df_sorted : pd.DataFrame
            DataFrame already sorted with SOMO rows first.
        logfolder : str
            Directory where the Excel file will be saved.
        logfile : str
            Name of the Gaussian log file used to generate the projection data.
        """
        
        # Convert 'β orbitals >X%' column (last dynamic key) into a string
        beta_colname = [col for col in df_sorted.columns if col.startswith("β orbitals >")][0]
        df_sorted[beta_colname] = df_sorted[beta_colname].apply(
            lambda lst: ", ".join([f"{idx}: {contrib:.1f}%" for idx, contrib in lst])
        )
    
        # Create Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Alpha→Beta Projections"
    
        yellow_fill = PatternFill(start_color="FFFF99", end_color="FFFF99", fill_type="solid")
    
        for r_idx, row in enumerate(dataframe_to_rows(df_sorted, index=False, header=True), 1):
            ws.append(row)
            if r_idx == 1:
                continue  # skip header
            if r_idx > 1 and row[-1] == "Yes":  # la colonne "SOMO?" est en dernière position
                for cell in ws[r_idx]:
                    cell.fill = yellow_fill
    
        output_path = Path(logfolder) / f"{Path(logfile).stem}_projection_sorted.xlsx"
        wb.save(output_path)
        print(f"✅ Saved to: {output_path}")


    alpha_df, beta_df, alpha_mat, beta_mat, nBasis, overlap_matrix, info = load_mos_from_cclib(logfolder, logfile)

    t4p.centerTitle("Computes the squared projection of each occupied alpha orbital onto the subspaces spanned by both virtual and occupied beta orbitals")

    # alpha_occ_idx = [i for i, occ in enumerate(alpha_df["Occupation"]) if occ == 'O']
    alpha_occ_idx = list(range(len(alpha_df)))

    alpha_occ_mat = alpha_mat[alpha_occ_idx, :]  # (n_occ_alpha, n_basis)
    beta_mat_all = beta_mat  # (n_beta, n_basis)

    projection_data = []
    for i, a in enumerate(alpha_occ_mat):
        proj_vec_all = a @ overlap_matrix @ beta_mat_all.T
        proj2_all = proj_vec_all**2
        norm2_total = float(np.dot(proj_vec_all, proj_vec_all))

        dominant_idx = int(np.argmax(proj2_all))
        norm2_occ = float(np.dot(a @ overlap_matrix @ beta_mat[[j for j, o in enumerate(beta_df["Occupation"]) if o == 'O']].T,
                                  a @ overlap_matrix @ beta_mat[[j for j, o in enumerate(beta_df["Occupation"]) if o == 'O']].T))
        norm2_virt = float(np.dot(a @ overlap_matrix @ beta_mat[[j for j, o in enumerate(beta_df["Occupation"]) if o == 'V']].T,
                                   a @ overlap_matrix @ beta_mat[[j for j, o in enumerate(beta_df["Occupation"]) if o == 'V']].T))

        sorted_proj2 = np.sort(proj2_all)[::-1]
        top1 = sorted_proj2[:1].sum()
        top2 = sorted_proj2[:2].sum()
        top3 = sorted_proj2[:3].sum()
        dominance_ratio = float(sorted_proj2[0] / norm2_total) if norm2_total > 0 else 0.0
        spread_flag = dominance_ratio < 0.6

        rel_contrib = proj2_all / norm2_total if norm2_total > 0 else np.zeros_like(proj2_all)
        significant_idx = [(j + 1, round(float(val * 100), 1)) for j, val in enumerate(rel_contrib) if val > threshold_beta/100]

        # is_somo = "Yes" if norm2_virt > 0.5 and norm2_occ < 0.5 else "No"
        occ_alpha = alpha_df.iloc[alpha_occ_idx[i]]["Occupation"]
        is_somo = "Yes" if (occ_alpha == "O" and norm2_virt > 0.5 and norm2_occ < 0.5) else "No"

        projection_data.append({
            "Alpha MO": alpha_occ_idx[i] + 1,
            "Occ α": alpha_df.iloc[alpha_occ_idx[i]]["Occupation"],
            "Energy (Ha)": alpha_df.iloc[alpha_occ_idx[i]]["Energy (Ha)"],
            "Projection² on β_virtual": float(f"{norm2_virt:.3f}"),
            "Projection² on β_occupied": float(f"{norm2_occ:.3f}"),
            "Dominant β MO": dominant_idx + 1,
            "Index4Jmol": dominant_idx + 1 + nBasis,
            "Occ β": beta_df.iloc[dominant_idx]["Occupation"],
            "E (β, Ha)": beta_df.iloc[dominant_idx]["Energy (Ha)"],
            "Top 1 contrib (%)": float(f"{100 * top1 / norm2_total:.1f}" if norm2_total > 0 else 0),
            "Top 2 contrib (%)": float(f"{100 * top2 / norm2_total:.1f}" if norm2_total > 0 else 0),
            "Top 3 contrib (%)": float(f"{100 * top3 / norm2_total:.1f}" if norm2_total > 0 else 0),
            "Dominance ratio": round(dominance_ratio, 3),
            "Spread?": "Yes" if spread_flag else "No",
            f"β orbitals >{threshold_beta}%": significant_idx,
            "SOMO?": is_somo
        })
    df = pd.DataFrame(projection_data)

    def custom_sort_alpha_df(df):
        """
        Trie le DataFrame des projections alpha → beta selon :
        - d'abord les alpha virtuelles (Occ α == "V")
        - ensuite les SOMOs (Occ α == "O" et SOMO? == "Yes")
        - puis les autres alpha occupées
        Chaque bloc est trié en Alpha MO décroissant.
        """
        df_virtuals = df[df["Occ α"] == "V"].copy()
        df_somos = df[(df["Occ α"] == "O") & (df["SOMO?"] == "Yes")].copy()
        df_others = df[(df["Occ α"] == "O") & (df["SOMO?"] != "Yes")].copy()
        
        df_virtuals = df_virtuals.sort_values(by="Alpha MO", ascending=False)
        df_somos = df_somos.sort_values(by="Alpha MO", ascending=False)
        df_others = df_others.sort_values(by="Alpha MO", ascending=False)
        return pd.concat([df_virtuals, df_somos, df_others], ignore_index=True)
   
    df_sorted = custom_sort_alpha_df(df)
    save_projection_results_to_excel(df_sorted, logfolder, logfile)
    return df_sorted, info

def show_alpha_to_homo(df_proj, logfolder, logfile, highlight_somo=True):
    """
    Affiche les lignes du DataFrame df_proj correspondant aux orbitales alpha
    allant de l’α 1 jusqu’à la HOMO, avec surlignage facultatif des SOMOs.

    Paramètres
    ----------
    df_proj : pd.DataFrame
        DataFrame contenant les résultats de projection alpha → beta.
    logfolder : str
        Dossier contenant le fichier log.
    logfile : str
        Nom du fichier log.
    highlight_somo : bool
        Si True, surligne les lignes avec SOMO? == "Yes".

    Retourne
    --------
    pd.DataFrame ou Styler
        Un sous-ensemble stylisé ou brut du DataFrame.
    """
    from .io import load_mos_from_cclib
    
    alpha_df, *_ = load_mos_from_cclib(logfolder, logfile)
    homo_alpha = max(i for i, occ in enumerate(alpha_df["Occupation"]) if occ == "O")
    homo_index = homo_alpha + 1  # indices dans df_proj sont 1-based
    filtered = df_proj[df_proj["Alpha MO"] <= homo_index].copy()

    if not highlight_somo:
        return filtered

    def somo_highlight(row):
        return ['background-color: #ffff99' if row["SOMO?"] == "Yes" else '' for _ in row]

    return filtered.style.apply(somo_highlight, axis=1)

#=========================================================
def compute_projection_matrix_and_eigenvalues(lMOs, cMOs, nbasis, overlap_matrix):
    """
    Computes the projection matrix P = A A^T where A = alpha · S · beta^T,
    and returns its eigenvalues and eigenvectors.

    Parameters
    ----------
    lMOs : np.ndarray 
    cMOs : np.ndarray
    nbasis : int
        Number of basis functions.
    overlap_matrix : np.ndarray
        AO overlap matrix (shape: n_basis, n_basis).

    Returns
    -------
    eigenvalues : np.ndarray
        Eigenvalues of the projection matrix P.
    eigenvectors : np.ndarray
        Eigenvectors of the projection matrix P.
    P : np.ndarray
        The projection matrix.
    """
    alpha_df = lMOs[0]
    beta_df = lMOs[1]
    alpha_mat = cMOs[0]
    beta_mat = cMOs[1]

    alpha_occ_idx = [i for i, occ in enumerate(alpha_df["Occupation"]) if occ == "O"]
    alpha_occ_mat = alpha_mat[alpha_occ_idx, :]

    # A = <alpha_occ | beta> : (n_alpha_occ × n_beta)
    A = alpha_occ_mat @ overlap_matrix @ beta_mat.T
    
    # P = A A† : (n_alpha_occ × n_alpha_occ)
    P = A @ A.T
    

    # Diagonalize P
    eigenvalues, eigenvectors = np.linalg.eigh(P)  # Use eigh since P is symmetric

    return eigenvalues[::-1], eigenvectors[:, ::-1], P  # Return in descending order

# Simulate a call with dummy values (the actual call should pass real data)
# compute_projection_matrix_and_eigenvalues(alpha_df, beta_df, alpha_mat, beta_mat, nbasis, overlap_matrix)

def compute_projection_matrix_and_eigenvalues(lMOs, cMOs, nbasis, overlap_matrix):
    """
    Computes the projection matrix P = A Aᵀ where A = alpha_occ · S · beta.T,
    and returns its eigenvalues and eigenvectors.

    Parameters
    ----------
    lMOs : tuple
        Tuple containing two DataFrames: (alpha_df, beta_df), each with MO occupations and energies.
    cMOs : tuple
        Tuple of two np.ndarrays: (alpha_mat, beta_mat), each of shape (n_OMs, n_basis).
        MOs are stored in rows (i.e., row i = MO_i).
    nbasis : int
        Number of basis functions.
    overlap_matrix : np.ndarray
        AO overlap matrix (shape: n_basis, n_basis).

    Returns
    -------
    eigenvalues : np.ndarray
        Eigenvalues of the projection matrix P.
    eigenvectors : np.ndarray
        Eigenvectors of the projection matrix P.
    P : np.ndarray
        The projection matrix P = A Aᵀ.
    """
    alpha_df, beta_df = lMOs
    alpha_mat, beta_mat = cMOs

    # Filter only occupied alpha orbitals
    occ_alpha_idx = [i for i, occ in enumerate(alpha_df["Occupation"]) if occ == "O"]
    alpha_occ = alpha_mat[occ_alpha_idx, :]  # (n_occ_alpha, n_basis)

    # Compute A = alpha_occ · S · beta.T
    A = alpha_occ @ overlap_matrix @ beta_mat.T  # (n_occ_alpha, n_beta)

    # Compute P = A Aᵀ
    P = A @ A.T  # (n_occ_alpha, n_occ_alpha)

    # Diagonalize
    eigenvalues, eigenvectors = np.linalg.eigh(P)

    return eigenvalues, eigenvectors, P

def compute_orbital_projections(lMOs, cMOs, overlap_matrix):
    """
    Computes how much each alpha orbital is represented in the beta orbital space
    using the AO overlap matrix S.

    Parameters
    ----------
    lMOs : tuple of DataFrames
        Tuple (alpha_df, beta_df), each containing orbital metadata.
    cMOs : tuple of np.ndarray
        Tuple (alpha_mat, beta_mat), each of shape (n_orbs, n_basis), with rows as orbitals.
    overlap_matrix : np.ndarray
        AO overlap matrix, shape (n_basis, n_basis).

    Returns
    -------
    pd.DataFrame
        DataFrame with alpha orbital number, energy, occupation, and squared projection norm.
    """
    alpha_df, beta_df = lMOs
    alpha_mat, beta_mat = cMOs

    projections = []
    for i, a in enumerate(alpha_mat):
        # Project orbital a onto the beta space
        A_i = a @ overlap_matrix @ beta_mat.T  # shape (n_beta,)
        proj_norm2 = np.dot(A_i, A_i)          # scalar: ||Proj_beta(a)||²

        projections.append({
            "Alpha OM": i + 1,
            "Energy (Ha)": alpha_df.iloc[i]["Energy (Ha)"],
            "Occupation": alpha_df.iloc[i]["Occupation"],
            "Projection²": proj_norm2
        })

    return pd.DataFrame(projections)

def print_eigen_analysis(eigenvalues, threshold=0.8):
    """
    Prints and analyzes the eigenvalues of the projection matrix.

    Parameters
    ----------
    eigenvalues : np.ndarray
        Eigenvalues of the projection matrix (real and ≥ 0).
    threshold : float
        Eigenvalues below this threshold are considered "low" (possible SOMO signature).
    """
    print("=== Projection Matrix Eigenvalue Analysis ===")
    print(f"Total eigenvalues: {len(eigenvalues)}")
    print()

    n_high = np.sum(eigenvalues > 0.95)
    n_low = np.sum(eigenvalues < threshold)

    for i, val in enumerate(sorted(eigenvalues, reverse=True)):
        status = ""
        if val > 0.95:
            status = "✅ well projected"
        elif val < threshold:
            status = "⚠️ low projection (possible SOMO)"
        else:
            status = "↔️ intermediate"

        print(f"Eigenvalue {i+1:2d}: {val:.3f} {status}")

    print()
    print(f"🔹 {n_high} strongly projected α-OMs")
    print(f"🔸 {n_low} possibly unpaired α-OMs (SOMO candidates)")

def identify_somos_from_projection(logfolder, logfile):
    """
    Identifies potential SOMOs by projecting occupied alpha orbitals onto the beta orbital space.

    Parameters
    ----------
    logfolder : str
        Path to the folder containing the Gaussian log file.
    logfile : str
        Name of the Gaussian .log file.

    This function:
    - Loads orbital data from the log file.
    - Computes the projection matrix P = A Aᵀ where A = α_occ · S · βᵀ.
    - Diagonalizes P and plots its eigenvalues.
    - Flags alpha orbitals with eigenvalues > 0.5 that project mainly onto virtual beta orbitals.
    """
    from .io import load_mos_from_cclib
    
    alpha_df, beta_df, alpha_mat, beta_mat, nBasis, overlap_matrix, info = load_mos_from_cclib(logfolder, logfile)
    n_alpha_occ = (alpha_df["Occupation"] == "O").sum()
    n_beta_occ = (beta_df["Occupation"] == "O").sum()
    alpha_occ_idx = [i for i, occ in enumerate(alpha_df["Occupation"]) if occ == 'O']
    alpha_occ_mat = alpha_mat[alpha_occ_idx, :]
    
    print(f"n_basis = {nBasis}")
    print(f"Occupied alpha MOs: {n_alpha_occ} (1 -> {n_alpha_occ})")
    print(f"Occupied beta MOs : {n_beta_occ} ({nBasis+1} -> {nBasis+n_beta_occ+1})")
    
    listMOs = (alpha_df, beta_df)
    coeffMOs = (alpha_mat, beta_mat)
    
    eigenvalues, eigenvectors, P = compute_projection_matrix_and_eigenvalues(listMOs, coeffMOs, nBasis, overlap_matrix)
    eigenvalues = np.clip(eigenvalues, 0, 1)

    
    plt.figure(figsize=(8, 5))
    plt.plot(eigenvalues, marker='o')
    plt.xlabel("Orbital index")
    plt.ylabel("Projection eigenvalue")
    plt.title("Eigenvalues of α → β projection matrix")
    plt.grid(True)
    plt.show()
    
    print(eigenvalues)
    
    A = alpha_occ_mat @ overlap_matrix @ beta_mat.T
    dominant_beta_index = np.argmax(A**2, axis=1)  # ou abs si non-normalisé
    for i, beta_idx in enumerate(dominant_beta_index):
        if beta_df.iloc[beta_idx]["Occupation"] == 'V' and eigenvalues[i] > 0.5:
            e_alpha = alpha_df.iloc[alpha_occ_idx[i]]["Energy (Ha)"]
            e_beta = beta_df.iloc[beta_idx]["Energy (Ha)"]
            print(f"🧲 OM alpha #{alpha_occ_idx[i]+1} (E={e_alpha:.3f} Ha) may be a SOMO — projects onto virtual beta #{beta_idx+1} (E={e_beta:.3f} Ha)")


# #### Heatmap

def parse_beta_contrib_string(s):
    if not isinstance(s, str) or not s.strip():
        return []
    parts = s.split(",")
    result = []
    for p in parts:
        try:
            idx, contrib = p.strip().split(":")
            idx = int(idx.strip())
            contrib = float(contrib.strip().replace("%", ""))
            result.append((idx, contrib))
        except Exception:
            continue
    return result

def projection_heatmap_from_df(df, nbasis, logfolder="./logs", logfile="logfile.log"):
    from ipywidgets import interact, interactive_output, IntSlider, Button, HBox, Checkbox, Output, VBox
    from functools import partial
    from .io import load_mos_from_cclib

    alpha_df, beta_df, alpha_mat, beta_mat, nBasis, overlap_matrix, info = load_mos_from_cclib(logfolder, logfile)
    lMOs = (alpha_df, beta_df)

    del alpha_mat, beta_mat, overlap_matrix, info, nBasis
    n_alpha_occ = (alpha_df["Occupation"] == "O").sum()
    n_beta_occ = (beta_df["Occupation"] == "O").sum()
    
    print(f"n_basis = {nbasis}")
    print(f"Occupied alpha MOs: {n_alpha_occ} (1 -> {n_alpha_occ})")
    print(f"Occupied beta MOs : {n_beta_occ} ({nbasis+1} -> {nbasis+n_beta_occ+1})")
    
    t4p.centerTitle("Main projection contribution of Alpha MOs on Beta MOs")

    fig_container = {"fig": None}
    output_msg = Output()
    output_msg.clear_output()

    def update_heatmap(n_occ, n_virt,n_beta_occ, n_beta_virt,
                       show_values,
                      ):
        alpha_indices = []
        beta_indices = set()
        contrib_dict = {}
        
        alpha_occ_idx = [i for i, occ in enumerate(lMOs[0]['Occupation']) if occ == 'O']
        beta_occ_idx = [i for i, occ in enumerate(lMOs[1]['Occupation']) if occ == 'O']
        homo_alpha = max(alpha_occ_idx)
        homo_beta = max(beta_occ_idx)
        lumo_beta = min([i for i, occ in enumerate(lMOs[1]['Occupation']) if occ == 'V'])

        selected_alpha_occ = list(range(max(0, homo_alpha - n_occ), homo_alpha + 1))
        selected_alpha_virt = list(range(homo_alpha + 1, homo_alpha + 1 + n_virt))
        selected_alpha = selected_alpha_occ + selected_alpha_virt

        beta_start = min(selected_alpha)

        selected_beta_occ = list(range(max(0, homo_beta - n_beta_occ), homo_beta + 1))
        selected_beta_virt = list(range(lumo_beta, lumo_beta + n_beta_virt))
        selected_beta = sorted(set(selected_beta_occ + selected_beta_virt + list(range(beta_start, homo_beta + 1))))

        for _, row in df.iterrows():
            alpha_idx = int(row["Alpha MO"])
            alpha_indices.append(alpha_idx)
            contribs = parse_beta_contrib_string(row[next(c for c in row.index if c.startswith("β orbitals >"))])
            contrib_dict[alpha_idx] = {b: w for b, w in contribs}
            beta_indices.update([b for b, _ in contribs])

        alpha_indices = sorted(alpha_indices)
        beta_indices = sorted(beta_indices)

        matrix = np.zeros((len(selected_alpha), len(selected_beta)))

        for i, a in enumerate(selected_alpha):
            for j, b in enumerate(selected_beta):
                matrix[i, j] = contrib_dict.get(a+1, {}).get(b+1, 0.0)/100

        y_labels = [f"α {i+1}" for i in selected_alpha]
        x_labels = [f"β {i+1}" for i in selected_beta]

        n_occ_alpha_in_plot = sum(1 for i in selected_alpha if lMOs[0].iloc[i]['Occupation'] == 'O')
        n_occ_beta_in_plot = sum(1 for i in selected_beta if lMOs[1].iloc[i]['Occupation'] == 'O')
        
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(matrix,
                    xticklabels=x_labels,
                    yticklabels=y_labels,
                    cmap="viridis",
                    annot=show_values,
                    fmt=".2f" if show_values else "",
                    ax=ax)
        ax.invert_yaxis()
        ax.axhline(n_occ_alpha_in_plot, color="red", linestyle="--", lw=1.5)
        ax.axvline(n_occ_beta_in_plot, color="red", linestyle="--", lw=1.5)

        ax.set_xlabel("Beta MOs")
        ax.set_ylabel("Alpha MOs")

        fig.tight_layout()
        fig_container["fig"] = fig
        plt.show()

    def save_heatmap(_):
        fig = fig_container.get("fig")
        if fig is not None:
            filename_prefix = Path(logfile).stem
            save_path = Path(logfolder) / f"{filename_prefix}_projection_heatmap.png"
            fig.savefig(save_path, dpi=300, transparent=True)
            with output_msg:
                output_msg.clear_output()
                display(Markdown(f"✅ **Image saved as `{save_path}`**"))
        else:
            with output_msg:
                output_msg.clear_output()
                display(Markdown("❌ **No figure to save.**"))

    save_button = Button(description="💾 Save map", tooltip=f"Save map to PNG in {logfolder}")
    save_button.on_click(save_heatmap)

    display(HBox([save_button]))
    display(output_msg)

    slider_alpha_occ = IntSlider(value=5, min=1, max=30, step=1,
                                 description="HOMO–n > HOMO", continuous_update=False)
    slider_alpha_virt = IntSlider(value=5, min=1, max=30, step=1,
                                  description="LUMO > LUMO+n", continuous_update=False)
    slider_beta_occ = IntSlider(value=0, min=0, max=30, step=1,
                                description="β HOMO–n > HOMO", continuous_update=False)
    slider_beta_virt = IntSlider(value=5, min=1, max=30, step=1,
                                 description="β LUMO > LUMO+n", continuous_update=False)
    show_values_checkbox = Checkbox(value=False, description="Show values", indent=False)

    interact(
        update_heatmap,
        n_occ=slider_alpha_occ,
        n_virt=slider_alpha_virt,
        n_beta_occ=slider_beta_occ,
        n_beta_virt=slider_beta_virt,
        show_values=show_values_checkbox
    )    

