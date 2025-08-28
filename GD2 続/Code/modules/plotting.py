import matplotlib.pyplot as plt
import numpy as np
import os

# この、モジュールは、関数を、定義するだけであり、直接、実行されることは、想定しない

def plot_money_plot(df_results, output_path, title_suffix=""):
    """
    指定された、パスに「マネープロット」を、生成し、保存する。
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(8, 8))
    
    ax.errorbar(df_results['dv_pred_mm_s'], df_results['dv_obs_mm_s'], yerr=df_results['dv_err_mm_s'], 
                fmt='o', capsize=5, color='royalblue', label=f'Spacecraft Data ({len(df_results)} Probes)')

    for name, row in df_results.iterrows():
        ax.text(row['dv_pred_mm_s'] + 0.3, row['dv_obs_mm_s'] - 0.3, name.replace('_', ' '), fontsize=9)
        
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
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig) # メモリを、解放
    print(f"\n[SUCCESS] Plot saved to: {output_path}")

def generate_theory_curves_plot(output_path):
    """
    指定された、パスに、理論曲線の、模式図を、生成し、保存する。
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(8, 6))

    lat_deg = np.linspace(-85, 85, 500)
    lat_rad = np.deg2rad(lat_deg)

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
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig) # メモリを、解放
    print(f"\n[SUCCESS] Theory curves plot saved to: {output_path}")