import numpy as np
from scipy.integrate import trapezoid
from astropy import units as u
from . import data_loader, geophysics

# --- 物理定数 ---
OMEGA_EARTH_RAD_S = 7.2921150e-5 # 地球の、自転角速度 (rad/s)

def calculate_physical_integrals(spacecraft_name):
    """
    指定された、探査機の、生の、軌道データから、GD理論の、各項に対応する、
    物理的な、積分値を、第一原理から、数値的に、計算する。
    """
    print(f"  > Calculating physical integrals for {spacecraft_name}...")
    
    # 1. 生の、軌道データを、ロード
    df = data_loader.load_trajectory_data(spacecraft_name)
    if df is None:
        raise FileNotFoundError(f"Could not load trajectory for {spacecraft_name}")

    # 2. 単位を、SI単位系に、統一し、Numpy配列へと、変換
    jd_tdb = df['JD_TDB'].values
    time_s = (jd_tdb - jd_tdb[0]) * 86400.0
    pos_icrf_m = df[['X_km', 'Y_km', 'Z_km']].values * 1000.0
    vel_icrf_ms = df[['VX_kms', 'VY_kms', 'VZ_kms']].values * 1000.0
    
    # 3. 軌道上の、各点における、物理量を、計算
    itrs_frames = geophysics.convert_icrf_to_itrs(jd_tdb, pos_icrf_m / 1000.0, vel_icrf_ms / 1000.0)
    
    pos_itrs_m = itrs_frames.cartesian.xyz.to(u.m).value.T
    vel_itrs_ms = itrs_frames.velocity.d_xyz.to(u.m/u.s).value.T
    lat_rad = np.deg2rad(itrs_frames.spherical.lat.degree)
    alt_m = itrs_frames.spherical.distance.to(u.m).value - 6.371e6
    b_itrs_T = geophysics.get_magnetic_field_itrs(itrs_frames)

    # 4. 各アノマリー成分の、被積分関数を、定義し、積分を実行
    #    これらは、ラグランジアンから、導出された、真の「力の、方程式」である
    
    # 4.1 回転項 (f_rot)
    v_norm = np.linalg.norm(vel_itrs_ms, axis=1, keepdims=True)
    v_hat = vel_itrs_ms / v_norm
    omega_vec_itrs = np.array([0, 0, OMEGA_EARTH_RAD_S])
    v_drag_ms = np.array([np.cross(omega_vec_itrs, p) for p in pos_itrs_m])
    integrand_rot = np.sum(v_drag_ms * v_hat, axis=1)
    f_rot = trapezoid(integrand_rot, time_s)

    # 4.2 ローレンツ共鳴項 (f_lor)
    integrand_lor = np.tan(np.abs(lat_rad))**2
    integrand_lor[np.abs(lat_rad) > np.deg2rad(85)] = np.tan(np.deg2rad(85))**2
    integrand_lor *= np.linalg.norm(vel_icrf_ms, axis=1)
    f_lor = trapezoid(integrand_lor, time_s)

    # 4.3 赤道ブレーキ項 (f_bra)
    v_cross_B = np.cross(vel_itrs_ms, b_itrs_T)
    integrand_brake = -np.sum(v_cross_B * v_hat, axis=1)
    f_brake = trapezoid(integrand_brake, time_s)
    
    # 4.4 太陽風項 (f_sol)
    alt_m[alt_m <= 0] = 1.0 
    integrand_solar = -1.0 / alt_m
    integrand_solar[alt_m > 50000e3] = 0 
    integrand_solar *= np.linalg.norm(vel_icrf_ms, axis=1)
    f_solar = trapezoid(integrand_solar, time_s)

    # 計算された、物理量を、辞書として、返す
    return {
        'rot': f_rot,
        'lor': f_lor,
        'bra': f_brake,
        'sol': f_solar,
    }