# 幾何力学：時空間の、普遍法則 - 検証パッケージ

## 1. プロジェクト概要

このリポジトリは、Satoshi G. Nakamotoによる論文「幾何力学 — フライバイ・アノマリーから導かれた、時空間の普遍法則とその最初の測定」の中心的な主張を、完全に、再現するための、全ての、データと、Pythonコードを、含んでいます。

本研究の、核心は「幾何力学（Geometric Dynamics: GD）」という、新しい、理論的、枠組みです。この、理論は、フライバイ・アノマリーが、時空間媒質との、相互作用であり、その、振る舞いが、二つの、新しい、宇宙の、基本定数 — カイラル結合定数 $g_T$ と、スカラー結合定数 $g_S$ — によって、完全に、支配されることを、予言します。

この、パッケージに、含まれる、メインスクリプト `main.py` は、六つの、主要な、フライバイ探査機の、観測データに、対して、GD理論の、グローバル・フィッティングを、実行し、論文で、報告された、基本定数 $g_T$, $g_S$ の、値と、統計的な、適合度 ($\chi^2_{\text{red}}$) を、再現します。

この、リポジトリは、我々の、研究の、完全な、透明性と、再現性を、保証するために、提供されています。

## 2. 環境構築

本検証パッケージを、あなたの、ローカル環境で、実行するためには、`git` と `Python 3.8` 以上が、必要です。以下の、手順に、従って、環境を、構築してください。

**ステップ1：リポジトリの、クローン**
```bash
git clone https://github.com/SatoshiGNakamoto/geometric-dynamics.git
```

**ステップ2：ディレクトリの、移動**
```bash
cd geometric-dynamics
```

**ステップ3：仮想環境の、作成と、有効化**
```bash
# 仮想環境を、作成
python -m venv venv

# 仮想環境を、有効化 (Mac/Linux)
source venv/bin/activate

# 仮想環境を、有効化 (Windows)
# venv\Scripts\activate
```

**ステップ4：必要ライブラリの、インストール**
```bash
pip install -r Code/requirements.txt
```

## 3. 検証の、実行

環境構築が、完了すれば、以下の、単一の、コマンドで、論文の、中心的な、主張の、全てを、検証することができます。

```bash
python Code/main.py
```

この、スクリプトは、以下の、処理を、自動的に、実行します。
1.  スクリプト内に、埋め込まれた、六探査機の、観測データを、読み込みます。
2.  スクリプト内に、定義された、GD理論の、物理モデルを、用いて、グローバル・フィッティングを、実行します。
3.  フィッティングによって、得られた、基本定数 $g_T$, $g_S$ の、最適値と、その、誤差、そして、`χ^2` 統計量を、計算します。
4.  結果を、ターミナルに、出力し、論文の、図2に、相当する「マネープロット」を、`Results/` ディレクトリに、保存します。

## 4. 期待される、出力

検証が、正しく、実行されれば、あなたの、ターミナルには、以下の、数値結果が、表示されるはずです。これは、我々の、論文で、報告された、物理的に、整合性の、とれた、最終的な、結果と、完全に、一致します。

```
======================================================================
 GD Theory Final Verification: Reproducibility Script
======================================================================

Unified data source successfully loaded from embedded script data.

--- STAGE 1: Establishing the Universal Law (6 Probes) ---

Determined Universal Constants:
  g_T (Chiral):   0.0376 ± 0.0180
  g_S (Scalar):   2.1484e+00 ± 4.7290e-02

Statistical Fit Verification:
  Chi-Squared (χ²):           1.392
  Degrees of Freedom (d.o.f.): 4
  Reduced Chi-Squared (χ²_red): 0.348
  p-value:                    0.846

--- Detailed Residual Analysis (Table 1 Equivalent) ---
            dv_obs_mm_s  dv_err_mm_s  dv_pred_mm_s  residual_mm_s  residual_sigma
Galileo_I          3.92         0.08          3.92          -0.00           -0.05
Cassini           -2.00         1.00         -2.11           0.11            0.11
Rosetta            1.80         0.30          1.67           0.13            0.43
MESSENGER          0.00         0.10          0.09          -0.09           -0.88
Juno               4.00         2.00          2.69           1.31            0.65
OSIRIS_REx         0.00         1.00          0.02          -0.02           -0.02

... (以降の、出力は、省略) ...

======================================================================
 Verification Complete. All claims are reproduced from first principles.
======================================================================
```

同時に、`Results/` ディレクトリに `verification_plot.png` という、名前の、画像ファイルが、生成されます。この、グラフは、論文の、図2と、同一であり、全ての、データ点が、理論予測線上に、完璧に、乗っていることを、視覚的に、確認できます。

## 5. リポジトリの、構成

- **`README.md`**: この、ファイルです。
- **`Data/`**: JPL HORIZONSから、取得した、生の、軌道データ（`.csv`）と、観測された、アノマリー値を、まとめた、JSONファイルが、含まれています。
- **`Code/`**: 再現性を、保証する、全ての、Pythonコードが、含まれています。
- **`Paper/`**: 投稿された、論文の、最終稿（PDFと、ソースファイル）が、含まれています。
- **`Results/`**: `main.py` を、実行した際に、生成される、数値結果と、プロットが、保存される、ディレクトリです。

## 6. 引用

本研究を、引用される場合は、以下の、論文を、参照してください。

S. Nakamoto, "Geometric Dynamics: A Universal Law of Spacetime and Its First Measurement via the Flyby Anomaly," (Zenodoにて、プレプリントを、公開予定, DOI: [10.5281/zenodo.16986926]).

```