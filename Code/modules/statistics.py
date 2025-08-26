import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import chi2

def unified_prediction_model(x_data, g_T, g_S):
    """
    GD理論の、核心となる、予測モデル関数。
    幾何学的、因子と、二つの、基本定数から、アノマリーを、予測する。
    """
    # 複数の、探査機の、因子を、一度に、受け取る
    # x_data は、(4, N_probes) の、形状を持つ、配列
    f_rot, f_lorentz, f_brake, f_solar = x_data
    
    # 論文の、補遺A2で、導出された、理論的な、係数
    # これらは、フィットされる、パラメータでは、なく、固定された、物理定数である
    C_rot   = 1.0 / (2 * np.pi)
    C_L     = 1.0 / (4 * np.pi)
    C_B     = -1.0 
    C_S     = -0.05 
    
    # アノマリーを、構成する、四つの、物理的な、成分を、計算
    dv_rot      = C_rot * g_S * f_rot
    dv_lorentz  = C_L * (g_T**2 / g_S) * f_lorentz
    dv_brake    = C_B * g_T * f_brake
    dv_solar    = C_S * g_S * f_solar
    
    # 最終的な、予測値は、これらの、線形和である。
    # 論文で、使用されている、mm/s の、単位に、合わせるため、スケール因子を、掛ける
    return (dv_rot + dv_lorentz + dv_brake + dv_solar) * 1e8

def perform_fit(factors, dv_obs, dv_err):
    """
    データに、対して、グローバルな、重み付き、最小二乗法フィットを、実行する。
    """
    # フィッティングの、ための、初期推測値
    initial_guess = [4.0, 2e-5] # g_T, g_S
    
    popt, pcov = curve_fit(
        f=unified_prediction_model,
        xdata=factors,
        ydata=dv_obs,
        sigma=dv_err,
        p0=initial_guess,
        absolute_sigma=True  # 誤差は、絶対的な、ものとして、扱う
    )
    
    return popt, pcov

def calculate_chi_squared(y_obs, y_pred, y_err, num_params):
    """
    カイ二乗値、自由度、reducedカイ二乗値、そして、p-valueを、計算する。
    """
    residuals = y_obs - y_pred
    chi_sq = np.sum((residuals / y_err)**2)
    dof = len(y_obs) - num_params
    # 自由度が、ゼロの、場合は、計算を、避ける
    if dof > 0:
        red_chi_sq = chi_sq / dof
        p_value = chi2.sf(chi_sq, dof)
    else:
        red_chi_sq = np.inf
        p_value = 0
    
    return chi_sq, dof, red_chi_sq, p_value