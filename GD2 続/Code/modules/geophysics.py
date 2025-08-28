import numpy as np
import pyIGRF
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import GCRS, ITRS, CartesianRepresentation, CartesianDifferential

def patch_astropy_iers():
    """Astropyの、IERSデータ、ダウンロードに関する、SSL証明書の、問題を、回避する。"""
    try:
        from astropy.utils.iers import conf
        conf.iers_auto_url_mirror = 'https://datacenter.iers.org/data/9/finals2000A.all'
        conf.iers_auto_url = conf.iers_auto_url_mirror
    except Exception:
        pass

patch_astropy_iers()

# --- 修正点：速度ベクトルも、引数として、受け取るように、関数を、再設計 ---
def convert_icrf_to_itrs(jd_tdb, pos_icrf_km, vel_icrf_kms):
    """
    状態ベクトル（位置と、速度）を、ICRFから、ITRSへと、変換する。
    """
    times = Time(jd_tdb, format='jd', scale='tdb')
    
    # --- 修正点：CartesianRepresentationに、速度情報(differentials)を、追加 ---
    cartesian_representation = CartesianRepresentation(
        pos_icrf_km.T * u.km,
        differentials=CartesianDifferential(vel_icrf_kms.T * u.km/u.s)
    )
    
    # GCRSフレームを、位置と、速度の、両方の、情報と、共に、作成
    gcrs_frames = GCRS(
        cartesian_representation,
        obstime=times
    )
    
    # ITRSへと、変換。速度情報も、自動的に、変換される。
    itrs_frames = gcrs_frames.transform_to(ITRS(obstime=times))
    
    return itrs_frames
# --- 修正、完了 ---

def get_magnetic_field_itrs(itrs_frames):
    """
    ITRS座標上の、各点における、地球磁場ベクトルを、IGRF-13モデルを、用いて、計算する。
    """
    lat_deg = itrs_frames.spherical.lat.degree
    lon_deg = itrs_frames.spherical.lon.degree
    alt_km = itrs_frames.spherical.distance.to(u.km).value - 6371.2 
    
    year_array = itrs_frames.obstime.decimalyear
    
    b_ned_list = [
        pyIGRF.igrf_value(lat, lon, alt, year)
        for lat, lon, alt, year in zip(lat_deg, lon_deg, alt_km, year_array)
    ]
    b_ned_nT = np.array([res[0:3] for res in b_ned_list])
    
    lat_rad, lon_rad = np.deg2rad(lat_deg), np.deg2rad(lon_deg)
    sin_lat, cos_lat = np.sin(lat_rad), np.cos(lat_rad)
    sin_lon, cos_lon = np.sin(lon_rad), np.cos(lon_rad)
    
    b_x = -b_ned_nT[:,0]*sin_lat*cos_lon - b_ned_nT[:,1]*sin_lon - b_ned_nT[:,2]*cos_lat*cos_lon
    b_y = -b_ned_nT[:,0]*sin_lat*sin_lon + b_ned_nT[:,1]*cos_lon - b_ned_nT[:,2]*cos_lat*sin_lon
    b_z =  b_ned_nT[:,0]*cos_lat - b_ned_nT[:,2]*sin_lat
    
    return np.vstack([b_x, b_y, b_z]).T * 1e-9