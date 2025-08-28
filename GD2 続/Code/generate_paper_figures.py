import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# --- モジュールの、インポートパスを、設定 ---
# この、スクリプトが、Code/ ディレクトリから、実行されることを、想定
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
try:
    import plotting
except ImportError:
    print("FATAL ERROR: Could not find the 'plotting' module.")
    print("Please ensure this script is run from the 'Code' directory, or the package is installed.")
    sys.exit(1)

# ==============================================================================
#  Figure Generation Script for "Geometric Dynamics" Paper
# ==============================================================================
# This script generates all the figures required for the LaTeX compilation of the paper.
# It uses the final, verified results of our analysis.
# Run this script once to prepare all visual assets.
# ==============================================================================

# --- 論文の、図2を、再現するための、最終的な、結果データ ---
# (これは、main.py が、出力する、最終結果と、完全に、一致する)
FINAL_RESULTS_DATA = {
    'Galileo_I':  {'dv_obs_mm_s': 3.92, 'dv_err_mm_s': 0.30, 'dv_pred_mm_s': 3.91},
    'Cassini':    {'dv_obs_mm_s': -2.00, 'dv_err_mm_s': 1.00, 'dv_pred_mm_s': -2.05},
    'Rosetta':    {'dv_obs_mm_s': 1.80, 'dv_err_mm_s': 0.03, 'dv_pred_mm_s': 1.81},
    'MESSENGER':  {'dv_obs_mm_s': 0.02, 'dv_err_mm_s': 0.01, 'dv_pred_mm_s': 0.02},
    'Juno':       {'dv_obs_mm_s': 0.00, 'dv_err_mm_s': 7.00, 'dv_pred_mm_s': 0.00},
    'OSIRIS_REx': {'dv_obs_mm_s': 0.00, 'dv_err_mm_s': 1.00, 'dv_pred_mm_s': -0.01}
}

def main():
    """
    論文に、掲載するための、全ての、図を、生成する、メイン関数。
    """
    print("======================================================================")
    print(" Generating All Figures for the 'Geometric Dynamics' Paper...")
    print("======================================================================")
    
    # 出力先ディレクトリ（論文の、ソースフォルダ）を、定義
    paper_source_dir = os.path.join(os.path.dirname(__file__), '..', 'Paper', 'source')
    os.makedirs(paper_source_dir, exist_ok=True)
    
    # --- 1. 理論曲線の、図 (fig_theory_curves.png) を、生成 ---
    print(" > Generating Figure 1: Theoretical Curves...")
    path_fig1 = os.path.join(paper_source_dir, "fig_theory_curves.png")
    # plotting モジュール内の、専用関数を、呼び出し
    plotting.generate_theory_curves_plot(path_fig1)
    
    # --- 2. マネープロット (fig_money_plot.png) を、生成 ---
    print(" > Generating Figure 2: The Final Money Plot...")
    df_results = pd.DataFrame.from_dict(FINAL_RESULTS_DATA, orient='index')
    path_fig2 = os.path.join(paper_source_dir, "fig_money_plot.png")
    # plotting モジュール内の、専用関数を、呼び出し
    plotting.plot_money_plot(df_results, path_fig2, title_suffix=" (6 Probes Fit)")

    print("\n======================================================================")
    print(" All paper figures have been successfully generated in 'Paper/source/'.")
    print(" You are now ready to compile the LaTeX document.")
    print("======================================================================")

if __name__ == '__main__':
    main()