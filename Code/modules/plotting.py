import matplotlib.pyplot as plt
import numpy as np
import os

# --- 出力先ディレクトリの、定義 ---
# 検証プロットは 'Results' フォルダへ
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'Results')
# 論文用の、静的な、図は 'Paper/source' フォルダへ
PAPER_SOURCE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'Paper', 'source')

# ディレクトリが、存在しない場合は、作成する
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(PAPER_SOURCE_DIR, exist_ok=True)


def plot_money_plot(df_results, title_suffix=""):
    """
    論文の、結論を、象徴する「マネープロット」（予測値 vs 観測値）を、生成し、保存する。
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(8, 8))
    
    ax.errorbar(df_results['dv_pred'], df_results['dv_obs_mm_s'], yerr=df_results['dv_err_mm_s'], 
                fmt='o', capsize=5, color='royalblue', label=f'Spacecraft Data ({len(df_results)} Probes)')

    for name, row in df_results.iterrows():
        ax.text(row['dv_pred'] + 0.3, row['dv_obs_mm_s'] - 0.3, name.replace('_', ' '), fontsize=9)
        
    lims = [
        np.floor(min(ax.get_xlim()[0], ax.get_ylim()[0]))-1,
        np.ceil(max(ax.get_xlim()[1], ax.get_ylim()[1]))+1
    ]
    ax.plot(lims, lims, 'k--', alpha=0.75, zorder=0, label='Perfect Agreement (y=x)')
    
    ax.set_aspect('equal')
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    
    ax.set_title(f'GD Theory: Prediction vs. Observation{title_suffix}', fontsize=16)
    ax.set_xlabel('Predicted $\Delta v$ [mm/s]', fontsize=12)
    ax.set_ylabel('Observed $\Delta v$ [mm/s]', fontsize=12)
    ax.legend(loc='upper left')
    
    # --- ファイル名を、'verification_plot.png' に、統一し、'Results' フォルダに、保存 ---
    filename = "verification_plot.png"
    file_path = os.path.join(RESULTS_DIR, filename)
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    print(f"\n[SUCCESS] Verification plot saved to: {file_path}")

def generate_theory_curves_plot():
    """
    論文の、図1に、相当する、理論曲線の、模式図を、生成し、保存する。
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(8, 6))

    lat_deg = np.linspace(-85, 85, 500)
    lat_rad = np.deg2rad(lat_deg)

    # 各効果の、模式的な、振る舞いを、定義
    rot_effect = np.ones_like(lat_deg) * 0.8
    brake_effect = -1.5 * np.cos(lat_rad)**2
    lorentz_effect = 0.1 * np.tan(np.abs(lat_rad))**2
    
    ax.plot(lat_deg, rot_effect, label='(a) Rotational Effect ($\propto g_S$)', linestyle='--')
    ax.plot(lat_deg, brake_effect, label='(b) Equatorial Brake ($\propto g_T$)', linestyle=':')
    ax.plot(lat_deg, lorentz_effect, label='(c) Lorentz Resonance ($\propto g_T^2/g_S$)', linestyle='-')
    
    ax.set_title('GD Anomaly Components vs. Latitude (Schematic)', fontsize=16)
    ax.set_xlabel('Latitude [degrees]', fontsize=12)
    ax.set_ylabel('Relative Contribution to $\Delta v$', fontsize=12)
    ax.set_ylim(-2, 5)
    ax.legend()
    ax.grid(True)
    
    # --- ファイル名を、'fig_theory_curves.png' に、固定し、'Paper/source' フォルダに、保存 ---
    filename = "fig_theory_curves.png"
    file_path = os.path.join(PAPER_SOURCE_DIR, filename)
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    print(f"\n[SUCCESS] Theory curves plot saved to: {file_path}")

# --- 修正点：これが、スクリプトを、直接、実行した際の「イグニッションキー」 ---
if __name__ == '__main__':
    # この、スクリプトを、直接、実行した場合、理論曲線を、生成する
    print("Generating theoretical curves plot for the paper...")
    try:
        generate_theory_curves_plot()
        print("\nOperation successful.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
# --- 修正、完了 ---