"""
Simulation 2 (formerly 3) — N_min for LEO orbits across SCS

Computes N_min = ceil(RTT / T_slot) + 1 for LEO 600 km and LEO 1200 km
across SCS 15/30/60/120 kHz, highlights cases exceeding max 32 processes.

Reference: Tuninato 2025, Section IV.A, Table 5
           TS 38.214 Section 5.1 (max 32 processes)
           TR 38.811 Table 5.3.4.1-1 (RTT values)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.harq.bler_model import TSLOT_MS
from src.harq.process_manager import n_min
from src.plots.plot_utils import savefig

# LEO orbits only
LEO_RTT_MS = {
    "LEO_600":  12.88,
    "LEO_1200": 24.32,
}
SCS_LIST = [15, 30, 60, 120]
MAX_PROC = 32


def run() -> None:
    print("\n" + "=" * 60)
    print("  Sim 2 — N_min for LEO orbits")
    print("=" * 60)

    # ── Compute table ───────────────────────────────────────────────────
    nmin_table = {}
    for orbit, rtt in LEO_RTT_MS.items():
        nmin_table[orbit] = {}
        for scs in SCS_LIST:
            nm = n_min(rtt, scs)
            nmin_table[orbit][scs] = {"n_min": nm, "feasible": nm <= MAX_PROC}

    # ── Print table ─────────────────────────────────────────────────────
    print("\n  N_min table (LEO, regenerative payload):")
    header = f"  {'Orbit':<14}" + "".join(f"{'SCS '+str(s)+' kHz':>12}" for s in SCS_LIST)
    print(header)
    print("  " + "-" * (14 + 12 * len(SCS_LIST)))
    for orbit, d in nmin_table.items():
        row = f"  {orbit:<14}"
        for scs in SCS_LIST:
            nm  = d[scs]["n_min"]
            tag = "x" if nm > MAX_PROC else " "
            row += f"{nm:>10}{tag} "
        print(row)
    print(f"  x = exceeds max {MAX_PROC} processes [TS 38.214, Section 5.1]")

    # ── Bar chart ────────────────────────────────────────────────────────
    orbits = list(nmin_table.keys())
    x = np.arange(len(orbits))
    width = 0.18
    colors = ["#2166ac", "#4dac26", "#d7191c", "#7b2d8b"]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for i, scs in enumerate(SCS_LIST):
        vals = [nmin_table[o][scs]["n_min"] for o in orbits]
        bars = ax.bar(x + i * width, vals, width,
                      label=f"SCS {scs} kHz", color=colors[i], alpha=0.85)
        for bar, v in zip(bars, vals):
            color = "red" if v > MAX_PROC else "black"
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    str(v), ha="center", va="bottom", fontsize=7.5, color=color,
                    fontweight="bold" if v > MAX_PROC else "normal")

    ax.axhline(MAX_PROC, color="red", lw=1.5, ls="--",
               label=f"Max N = {MAX_PROC} (TS 38.214)")
    ax.set_xticks(x + width * (len(SCS_LIST) - 1) / 2)
    orbit_labels = [o.replace("_", " ") for o in orbits]
    ax.set_xticklabels(orbit_labels)
    ax.set_ylabel("$N_{min}$ (HARQ processes)")
    ax.set_title("Minimum HARQ Processes to Avoid Pipeline Stall\n"
                 "[LEO, Regenerative Payload, Elevation 10°]")
    ax.legend(fontsize=8.5)
    ax.grid(True, axis="y", alpha=0.4)
    fig.tight_layout()
    savefig(fig, "sim03_nmin_leo")

    # ── Save data ────────────────────────────────────────────────────────
    out = Path(__file__).parents[2] / "results" / "data"
    flat = {}
    for orbit, d in nmin_table.items():
        for scs, vals in d.items():
            flat[f"{orbit}_scs{scs}_nmin"]    = vals["n_min"]
            flat[f"{orbit}_scs{scs}_feasible"] = vals["feasible"]
    np.savez(out / "sim03_nmin.npz", **flat)
    print("  Data saved → results/data/sim03_nmin.npz")
    print("  Sim 2 complete.")


if __name__ == "__main__":
    run()
