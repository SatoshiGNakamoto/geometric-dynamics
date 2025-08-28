import pandas as pd
import json
import os
from io import StringIO

# このファイルの、場所を、基準に、Dataディレクトリへの、相対パスを、定義
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'Data')

def load_trajectory_data(spacecraft_name):
    """
    指定された、探査機の、軌道データを、CSVファイルから、読み込み、整形する。
    JPL HORIZONS形式の、ヘッダー（$$SOE）と、フッター（$$EOE）を、自動的に、除去する。
    """
    file_path = os.path.join(DATA_DIR, f"{spacecraft_name}_clean.csv")
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Trajectory file not found at {file_path}")
        return None
        
    # データブロックの、開始行と、終了行を、見つける
    try:
        start_index = next(i for i, line in enumerate(lines) if line.strip().startswith('$$SOE')) + 1
        end_index = next(i for i, line in enumerate(lines) if line.strip().startswith('$$EOE'))
    except StopIteration:
        raise ValueError(f"Could not find SOE/EOE markers in {file_path}")
    
    data_lines = lines[start_index:end_index]
    
    # JPL HORIZONSの、出力形式に、基づいて、列名を、定義
    columns = [
        'JD_TDB', 'CalendarDate', 'LT', 'X_km', 'Y_km', 'Z_km', 'VX_kms', 'VY_kms', 'VZ_kms'
    ]
    
    # 文字列リストを、インメモリの、ファイルのように、扱い、pandasで、読み込む
    df = pd.read_csv(StringIO(''.join(data_lines)), header=None, names=columns)
    
    # 必要な、数値列のみを、選択し、型を、正しく、変換する
    df_numeric = df[['JD_TDB', 'X_km', 'Y_km', 'Z_km', 'VX_kms', 'VY_kms', 'VZ_kms']].astype(float)
    
    return df_numeric

def load_observed_anomalies():
    """観測された、アノマリーの、値を、JSONファイルから、読み込む。"""
    file_path = os.path.join(DATA_DIR, 'OBSERVED_ANOMALIES.json')
    try:
        with open(file_path, 'r') as f:
            anomalies = json.load(f)
    except FileNotFoundError:
        print(f"Error: Anomaly file not found at {file_path}")
        return None
    return anomalies