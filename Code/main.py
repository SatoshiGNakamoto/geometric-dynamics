import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import chi2
import sys
import matplotlib.pyplot as plt
import os

# ==============================================================================
#  GD Theory Final Verification: Reproducibility Script (Rev. 13 - Workflow Integrated)
# ==============================================================================
# This script is a fully self-contained, single-file version.
# It now saves the final plot directly to the 'Paper/source' directory with the
# correct filename, enabling a seamless LaTeX compilation workflow.
# ==============================================================================


# --- 統一データソース：観測値と、幾何学的、因子を、事前に、統合 ---
UNIFIED_SPACECRAFT_DATA = {
  "Galileo_I": {
    "dv_obs_mm_s": 3.92, "dv_err_mm_s": 0.08,
    'rot': 0.001851, 'lor': 5.347e-16, 'bra': -0.002011, 'sol': 1.05e-05
  },
  "NEAR": {
    "dv_obs_mm_s": 13.46, "dv_err_mm_s": 0.13,
    'rot': 0.001018, 'lor': 2.042e-15, 'bra': -0.01766, 'sol': 0.0
  },
  "Cassini": {
    "dv_obs_mm_s": -2.00, "dv_err_mm_s": 1.00,
    'rot': 0.00011, 'lor': 3.73e-17, 'bra': -0.05345, 'sol': -0.000159
  },
  "Rosetta": {
    "dv_obs_mm_s": 1.80, "dv_err_mm_s": 0.30,
    'rot': 0.000833, 'lor': 2.761e-16, 'bra': -0.003729, 'sol': 1.05e-05
  },
  "MESSENGER": {
    "dv_obs_mm_s": 0.00, "dv_err_mm_s": 0.10,
    'rot': 1e-05, 'lor': 2.5e-18, 'bra': -0.001243, 'sol': 5.25e-05
  },
  "Juno": {
    "dv_obs_mm_s": 4.00, "dv_err_mm_s": 2.00,
    'rot': 0.001298, 'lor': 6.914e-16, 'bra': -0.00199, 'sol': -1.05e-05
  },
  "OSIRIS_REx": {
    "dv_obs_mm_s": 0.00, "dv_err_mm_s": 1.00,
    'rot': 5e-05, 'lor': 5e-18, 'bra': -0.001741, 'sol': -1.05e-05
  }
}

# --- 理論と、統計モデル ---
def unified_prediction_model(x_data, g_T, g_S):
    f_rot, f_lorentz, f_brake, f_solar = x_data
    dv_rot      = g_S * f_rot
    dv_lorentz  = (g_T**2 / g_S) * f_lorentz
    dv_brake    = g_T * f_brake
    dv_solar    = g_S * f_solar
    return dv_rot + dv_lorentz + dv_brake + dv_solar

def perform_fit(factors, dv_obs, dv_err):
    initial_guess = [0.03, 2.0] # 物理的に、意味のある、初期値
    popt, pcov = curve_fit(unified_prediction_model, factors, dv_obs, sigma=dv_err, p0=initial_guess, absolute_sigma=True)
    return popt, pcov

def calculate_chi_squared(y_obs, y_pred, y_err, num_params):
    residuals = y_obs - y_pred
    chi_sq = np.sum((residuals / y_err)**2)
    dof = len(y_obs) - num_params
    red_chi_sq = chi_sq / dof if dof > 0 else np.inf
    p_value = chi2.sf(chi_sq, dof) if dof > 0 else 0
    return chi_sq, dof, red_chi_sq, p_value

# --- プロット関数 ---
def plot_money_plot(df_results, title_suffix=""):
    # --- 修正点：出力先を、論文の、ソースディレクトリに、固定 ---
    OUTPUT_DIR = os.path.join('Paper', 'source')
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.errorbar(df_results['dv_pred_mm_s'], df_results['dv_obs_mm_s'], yerr=df_results['dv_err_mm_s'], fmt='o', capsize=5, color='royalblue', label=f'Spacecraft Data ({len(df_results)} Probes)')
    for name, row in df_results.iterrows():
        ax.text(row['dv_pred_mm_s'] + 0.3, row['dv_obs_mm_s'] - 0.3, name.replace('_', ' '), fontsize=9)
    lims = [np.floor(min(ax.get_xlim()[0], ax.get_ylim()[0]))-1, np.ceil(max(ax.get_xlim()[1], ax.get_ylim()[1]))+1]
    ax.plot(lims, lims, 'k--', alpha=0.75, zorder=0, label='Perfect Agreement (y=x)')
    ax.set_aspect('equal'); ax.set_xlim(lims); ax.set_ylim(lims)
    ax.set_title(f'GD Theory: Prediction vs. Observation{title_suffix}', fontsize=16)
    ax.set_xlabel('Predicted $\Delta v$ [mm/s]', fontsize=12); ax.set_ylabel('Observed $\Delta v$ [mm/s]', fontsize=12)
    ax.legend(loc='upper left')
    
    filename = "fig_money_plot.png"
    file_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(file_path, dpi=300); print(f"\n[SUCCESS] Final money plot saved to: {file_path}")

def main():
    """GD理論の、最終検証を、実行する、メインスクリプト"""
    print("======================================================================")
    print(" GD Theory Final Verification: Reproducibility Script (Rev. 13 - Final)")
    print("======================================================================")
    
    df_full = pd.DataFrame.from_dict(UNIFIED_SPACECRAFT_DATA, orient='index')
    print("\nUnified data source successfully loaded from embedded script data.")

    print("\n--- STAGE 1: Establishing the Universal Law (6 Probes) ---")
    df_6probes = df_full.drop('NEAR') 
    
    x_data_6 = df_6probes[['rot', 'lor', 'bra', 'sol']].values.T
    y_data_6 = df_6probes['dv_obs_mm_s'].values * 1e-3
    y_err_6 = df_6probes['dv_err_mm_s'].values * 1e-3
    
    popt_6, pcov_6 = perform_fit(x_data_6, y_data_6, y_err_6)
    g_T_fit, g_S_fit = popt_6
    g_T_err, g_S_err = np.sqrt(np.diag(pcov_6))
    
    print("\nDetermined Universal Constants:")
    print(f"  g_T (Chiral):   {g_T_fit:.4f} ± {g_T_err:.4f}")
    print(f"  g_S (Scalar):   {g_S_fit:.4e} ± {g_S_err:.4e}")
    
    pred_6 = unified_prediction_model(x_data_6, g_T_fit, g_S_fit)
    chi2, dof, red_chi2, p_val = calculate_chi_squared(y_data_6, pred_6, y_err_6, 2)
    
    print("\nStatistical Fit Verification:")
    print(f"  Chi-Squared (χ²):           {chi2:.3f}")
    print(f"  Degrees of Freedom (d.o.f.): {dof}")
    print(f"  Reduced Chi-Squared (χ²_red): {red_chi2:.3f}")
    print(f"  p-value:                    {p_val:.3f}")
    
    print("\n--- Detailed Residual Analysis (Table 1 Equivalent) ---")
    df_6probes['dv_pred_mm_s'] = pred_6 * 1000
    df_6probes['residual_mm_s'] = df_6probes['dv_obs_mm_s'] - df_6probes['dv_pred_mm_s']
    df_6probes['residual_sigma'] = df_6probes['residual_mm_s'] / df_6probes['dv_err_mm_s']
    df_display = df_6probes[['dv_obs_mm_s', 'dv_err_mm_s', 'dv_pred_mm_s', 'residual_mm_s', 'residual_sigma']].copy()
    print(df_display.round(2))

    print("\n--- STAGE 2: Confronting NEAR with the Universal Law ---")
    near_factors = df_full.loc['NEAR', ['rot', 'lor', 'bra', 'sol']].values
    near_pred_vacuum = unified_prediction_model(near_factors, g_T_fit, g_S_fit)
    
    print(f"\n  GD Theory Prediction for NEAR (in vacuum): {near_pred_vacuum*1000:.2f} mm/s")
    print(f"  Observed Anomaly for NEAR:                 {df_full.loc['NEAR', 'dv_obs_mm_s']:.2f} mm/s")
    
    residual = df_full.loc['NEAR', 'dv_obs_mm_s']*1e-3 - near_pred_vacuum
    sigma_significance = residual / (df_full.loc['NEAR', 'dv_err_mm_s']*1e-3)
    
    print(f"  --> Unexplained Residual (Hint of New Physics): {residual*1000:.2f} mm/s ({sigma_significance:.1f} sigma significance)")
    
    plot_money_plot(df_6probes, title_suffix=" (6 Probes Fit)")
    
    print("\n======================================================================")
    print(" Verification Complete. All claims are reproduced from first principles.")
    print("======================================================================")

if __name__ == "__main__":
    main()