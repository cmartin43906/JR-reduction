# Neural Mass Modeling – Dynamical Analysis

This project implements and analyzes a reduced excitatory–inhibitory (E–I) neural mass model. The focus is on understanding how population interactions produce different dynamical regimes and how those dynamics relate to EEG-like signals.

---

# Structure

neural-mass/
├── .venv/
├── figures/
├── report/
├── src/
│   ├── main.py
│   ├── visualization.py
│   └── models/
│       ├── reduced.py
│       └── jansenrit.py
├── requirements.txt
├── .gitignore
└── README.md

---

# Setup

python3 -m venv .venv
source .venv/bin/activate      # macOS / Linux
# or
.venv\Scripts\activate         # Windows

pip install -r requirements.txt

---

# To Run

python src/main.py

This will:

* run simulations for multiple parameter regimes
* generate phase-plane, time-domain, and spectral plots
* print brief explanations to the terminal

---

## Overview

The project implements a reduced 2D E–I model used for phase-plane analysis. It explores:

* stable fixed points
* damped oscillations
* limit cycles

and how these behaviors change with:

* coupling strength (g)
* external drive (P_E)
* inhibitory timescale (τ_I)

A higher-dimensional Jansen–Rit model is included for reference.

---
