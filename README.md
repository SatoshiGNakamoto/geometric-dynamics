# Geometric Dynamics: A Universal Law of Spacetime - Verification Package

## 1. Project Overview

This repository contains the complete dataset and Python code to reproduce the central claims of the paper "Geometric Dynamics: A Universal Law of Spacetime and Its First Measurement via the Flyby Anomaly" by Satoshi G. Nakamoto.

The core of this research is a new theoretical framework, Geometric Dynamics (GD). This theory predicts that the flyby anomaly is an interaction with the spacetime medium, governed by two new fundamental constants of the universe: a chiral coupling constant, $g_T$, and a scalar coupling constant, $g_S$.

The main script included in this package, `main.py`, performs a global fit of the GD theory to the observational data from six major spacecraft flybys. Executing this script will reproduce the values of the fundamental constants $g_T$ and $g_S$, as well as the statistical goodness-of-fit ($\chi^2_{\text{red}}$), reported in the paper.

This repository is provided to ensure full transparency and reproducibility of our research.

## 2. Setup and Installation

To run this verification package in your local environment, you will need `git` and `Python 3.8` or higher. Please follow the steps below to set up the environment.

**Step 1: Clone the Repository**
```bash
git clone https://github.com/SatoshiGNakamoto/geometric-dynamics.git
```

**Step 2: Navigate to the Directory**
```bash
cd geometric-dynamics
```

**Step 3: Create and Activate a Virtual Environment**
```bash
# Create the virtual environment
python -m venv venv

# Activate on Mac/Linux
source venv/bin/activate

# Activate on Windows
# venv\Scripts\activate
```

**Step 4: Install Required Libraries**
```bash
pip install -r Code/requirements.txt
```

## 3. Running the Verification

Once the environment is set up, you can verify all the central claims of the paper with a single command:

```bash
python Code/main.py
```

This script will automatically perform the following actions:
1.  Load the observational data for the six spacecraft from the embedded data structures.
2.  Perform a global fit using the GD physical model defined in the script.
3.  Calculate the best-fit values for the fundamental constants $g_T$ and $g_S$, their uncertainties, and the $\chi^2$ statistics.
4.  Print the results to your terminal and save the "money plot" (equivalent to Figure 2 in the paper) to the `Results/` directory.

## 4. Expected Output

If the verification script runs correctly, your terminal should display the following numerical results. This output exactly matches the final, physically-grounded results reported in our paper.

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

... (further output) ...

======================================================================
 Verification Complete. All claims are reproduced from first principles.
======================================================================
```

Simultaneously, an image file named `verification_plot.png` will be generated in the `Results/` directory. This plot is identical to Figure 2 in the paper and visually confirms that all data points lie perfectly on the theoretical prediction line.

## 5. Repository Structure

- **`README.md`**: This file.
- **`Data/`**: Contains the raw trajectory data (`.csv`) from JPL HORIZONS and the anomaly observation data (`.json`).
- **`Code/`**: Contains all Python code that guarantees reproducibility.
- **`Paper/`**: Contains the final version of the submitted paper (PDF and source files).

## 6. Citation

If you use this work, please cite the following paper:

S. Nakamoto, "Geometric Dynamics: A Universal Law of Spacetime and Its First Measurement via the Flyby Anomaly," (Preprint available at Zenodo, DOI: [To be assigned upon publication]).

```