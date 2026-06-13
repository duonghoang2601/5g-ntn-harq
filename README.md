# Evaluating HARQ Efficiency in 5G Non-Terrestrial Networks (NTN)

> **Course project** — Satellite Communications (Thông tin vệ tinh)  
> Hanoi University of Science and Technology (ĐHBK Hà Nội) · School of Electrical and Electronic Engineering  
> Author: Vũ Thị Gấm (2024) · Supervisors: Nguyễn Hoàng Hải, Lâm Hồng Thạch

The full report (Vietnamese, PDF) is at [`report/main.pdf`](report/main.pdf).

---

## Overview

5G NR reuses the same HARQ protocol for both terrestrial and satellite links. This works fine on the ground (RTT < 1 ms), but satellite RTTs range from **13 ms (LEO 600 km)** to **270 ms (GEO 35 786 km)** — hundreds of times larger. This project quantifies the consequences through Monte Carlo simulation across five performance dimensions.

### Key findings

| Metric | Result |
|--------|--------|
| IR-HARQ link gain vs No-HARQ (4 TX, MCS A, BLER = 10⁻³) | **8.3 dB** |
| IR advantage over CC-HARQ | 0.5 dB (MCS A) · 1.2 dB (MCS B) |
| Orbit–SCS combinations feasible with N ≤ 32 | **3 / 16** (LEO only) |
| GEO pipeline utilisation (SCS 30 kHz, N = 32) | **5.89 %** |
| SE Goodput gain from disabling HARQ at GEO | **16.7×** (0.030 → 0.500 bit/s/Hz) |
| Energy-per-bit improvement vs No-HARQ at −5 dB | **~10⁹×** |

---

## Project structure

```
5g-ntn-harq/
│
├── run_all.py                  # Master runner — executes all 5 simulations
├── requirements.txt
│
├── src/                        # Simulation library
│   ├── channel/
│   │   └── lms_channel.py      # Rician i.i.d. channel model (TR 38.811)
│   ├── harq/
│   │   ├── bler_model.py       # MI-threshold BLER model (CC & IR)
│   │   └── process_manager.py  # N-process pipeline, util, SE Goodput, E_bit
│   ├── plots/
│   │   └── plot_utils.py       # Publication-quality figure helpers
│   └── sim/
│       ├── sim_01_bler_vs_snr.py       # Experiment 1 — BLER waterfall curves
│       ├── sim_02_throughput_vs_rtt.py # Experiment 2 — SE Goodput vs RTT
│       ├── sim_03_nmin.py              # Experiment 3 — N_min feasibility map
│       ├── sim_04_geo_disable.py       # Experiment 4 — GEO: HARQ vs RLC ARQ
│       └── sim_05_energy.py            # Experiment 5 — Energy per bit
│
├── results/
│   ├── data/          # Saved .npz arrays (re-plot without re-running MC)
│   └── figures/       # PDF + PNG outputs (used by the LaTeX report)
│
├── report/            # LaTeX source
│   ├── main.tex                # Top-level document
│   ├── main.pdf                # Compiled output (committed for convenience)
│   ├── references.bib          # BibTeX database
│   ├── IEEEtran.bst            # Bibliography style (ieeetr workaround)
│   ├── 2_bvp_logo_bk_rgb_148177.jpg  # HUST school logo
│   ├── frontmatter/
│   │   ├── cover.tex
│   │   ├── abstract.tex
│   │   ├── preface.tex
│   │   └── abbreviations.tex
│   └── chapters/
│       ├── ch1_intro.tex
│       ├── ch2_theory.tex      # ARQ/HARQ theory, Rician channel, pipeline math
│       ├── ch3_method.tex      # Monte Carlo methodology
│       ├── ch4_results.tex     # All five experiments with analysis
│       └── ch5_conclusion.tex
│
├── notebooks/         # Markdown study notes (background reading)
│   ├── 00_problem_statement.md
│   ├── 01_arq_to_harq.md
│   ├── 02_harq_cc_vs_ir.md
│   ├── 03_what_is_ntn.md
│   ├── 04_ntn_breaks_harq.md
│   ├── 05_3gpp_standards.md
│   ├── 06_channel_model_lms.md
│   ├── 07_parameter_selection.md
│   ├── 08_module_design.md
│   ├── 09_evaluation_criteria.md
│   ├── 10_results_interpretation.md
│   └── 11_conclusions.md
│
└── ref/               # Reference documents (3GPP specs, IEEE papers)
    ├── 3gpp/          # TS 38.212 / 38.214 / 38.811 / 38.821
    ├── ieee/          # Tuninato 2025 — key benchmark paper
    └── external/      # Supplementary reading
```

---

## Prerequisites

- Python ≥ 3.10
- A TeX Live installation with XeLaTeX (for compiling the report)

```bash
pip install -r requirements.txt
```

The four Python dependencies are: `numpy`, `scipy`, `matplotlib`, `tqdm`.

---

## Running the simulations

### Run everything at once

```bash
python run_all.py
```

This executes all five experiments in sequence (~5–15 min depending on hardware).  
Outputs go to `results/figures/` (PDF + PNG) and `results/data/` (`.npz` arrays).

### Run individual experiments

```bash
python run_all.py 1        # BLER vs Es/N0  (both MCS A and MCS B)
python run_all.py 2 4 5    # multiple experiments in one call
```

| ID | Name | Output files |
|----|------|-------------|
| 1 | BLER vs Es/N0 | `sim01_bler_vs_snr_mcs_{a,b}.{pdf,png}` |
| 2 | SE Goodput vs RTT | `sim02_throughput_vs_rtt{_annotated}.{pdf,png}` |
| 3 | N_min feasibility | `sim03_nmin_chart.{pdf,png}` |
| 4 | GEO HARQ vs RLC ARQ | `sim04_geo_disable.{pdf,png}` |
| 5 | Energy per bit | `sim05_energy_per_bit{_orbits}.{pdf,png}` |

### Re-plot from saved data (no Monte Carlo)

Each simulation saves its results to `results/data/*.npz`. To regenerate figures without re-running the heavy Monte Carlo:

```python
import numpy as np
from src.plots.plot_utils import plot_geo_disable, savefig

d = np.load("results/data/sim04_geo_disable.npz")
results = {
    "harq": {"bler": d["harq_bler"], "se_gp": d["harq_se"],
             "latency": d["harq_latency"], "utilization": 32/543},
    "rlc":  {"bler": d["rlc_bler"],  "se_gp": d["rlc_se"],
             "latency": d["rlc_latency"]},
}
fig = plot_geo_disable(d["snr_db"], results)
savefig(fig, "sim04_geo_disable")
```

---

## Compiling the report

```bash
cd report
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex      # third pass stabilises cross-refs and TOC
```

**Requirements:** XeLaTeX (TeX Live 2020+), Times New Roman or Latin Modern Roman.  
`IEEEtran.bst` is included in the repo because the system TeX Live installation may not have it.

The compiled PDF is committed at [`report/main.pdf`](report/main.pdf).

---

## Code walkthrough

### Channel model — `src/channel/lms_channel.py`

Generates i.i.d. Rician fading realisations:

```
h = sqrt(K/(K+1)) * exp(jφ)  +  sqrt(1/(K+1)) * (g_I + j*g_Q) / sqrt(2)
```

with `E[|h|²] = 1` exactly. Parameters match TR 38.811 Table 6.7.1-1 (Ka-band LMS, K = 15 dB).

### BLER model — `src/harq/bler_model.py`

MI-threshold model with LDPC gap Δ = 1.5 dB (Richardson & Urbanke):

- **CC-HARQ:** success when `(1/r) · log₂(1 + Σγᵢ/Δ) ≥ 1`  
- **IR-HARQ:** success when `(1/r) · Σ log₂(1 + γᵢ/Δ) ≥ 1`

IR ≥ CC by Jensen's inequality (log₂ is concave), with equality only at TX = 1.

### Pipeline manager — `src/harq/process_manager.py`

```
N_min  = ceil(RTT / T_slot) + 1
util   = min(1, N / N_min)
SE_GP  = util × (1 − BLER_final) × r × log₂(M)
E_bit  = P_tx × avg_ntx × T_slot / (util × (1 − BLER_final))
```

RTT values (regenerative payload, 10° elevation) from TR 38.811 Table 5.3.4.1-1:

| Orbit | Altitude | RTT |
|-------|----------|-----|
| LEO | 600 km | 12.88 ms |
| LEO | 1 200 km | 24.32 ms |
| MEO | 10 000 km | 93.45 ms |
| GEO | 35 786 km | 270.57 ms |

---

## Standards and references

| Document | What it specifies |
|----------|------------------|
| 3GPP TS 38.212 | LDPC codes, RV sequence {0,2,3,1} |
| 3GPP TS 38.214 | Max HARQ processes = 32, MCS tables |
| 3GPP TR 38.811 | NTN channel model, orbit RTT values |
| 3GPP TR 38.821 | HARQ-disable recommendation for GEO/MEO |
| Tuninato 2025 (IEEE Access) | Benchmark paper — HARQ vs RLC ARQ over satellite |

---

## Contributing

1. Fork and clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Make changes to `src/` or `report/`.
4. Run `python run_all.py` to verify simulation outputs are unchanged.
5. Compile the report (`xelatex` × 3) and check the PDF.
6. Submit a pull request with a clear description of what changed and why.

**Coding conventions**
- All simulation parameters are at the top of each `sim_0X.py` file — change them there, not inside functions.
- Physical constants and orbit RTT values live in `src/channel/lms_channel.py` (`ORBIT_RTT_MS`).
- Figures must use `savefig()` from `plot_utils.py` to guarantee consistent DPI and output paths.

---

## License

This project is course work submitted at HUST. Feel free to use the code for educational purposes.
