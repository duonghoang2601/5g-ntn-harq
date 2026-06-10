"""
Simulation 3 — Minimum HARQ Process Count Optimisation

Computes and visualises N_min = ⌈RTT / T_slot⌉ + 1 for every
orbit × SCS combination, highlights which cases exceed the
5G NR maximum of 32 processes (pipeline stall region).

Also plots SE as function of N for each orbit at a fixed SNR,
showing the "elbow" point where adding more processes no longer helps.

Reference: Tuninato 2025, Section IV.A and Table 5
           TS 38.214, Section 5.1 (max 16/32 processes)
           TR 38.811, Tables 5.3.4.1-1 and 5.3.2.1-1 (RTT values)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

import numpy as np
import matplotlib.pyplot as plt

from src.channel.lms_channel import ChannelConfig, ORBIT_RTT_MS
from src.harq.bler_model import HARQConfig, TSLOT_MS
from src.harq.process_manager import (
    simulate_nmin_table, n_min, pipeline_utilization,
    simulate_throughput_vs_rtt,
)
from src.plots.plot_utils import plot_nmin_chart, savefig, COLORS, LINESTYLES, MARKERS

SCS_LIST = [15, 30, 60, 120]
MAX_PROC = 32
CH       = ChannelConfig(K_dB=15.0, speed_kmh=50.0, fc_GHz=20.0)
IR_CFG   = HARQConfig(code_rate=1/2, max_retx=3, scheme="IR")
SNR_OP   = 5.0


def run() -> None:
    print("\n" + "="*60)
    print("  Sim 3 — N_min Optimisation")
    print("="*60)

    # ── Table of N_min ──────────────────────────────────────────────────
    nmin_table = simulate_nmin_table(SCS_LIST, max_proc=MAX_PROC)

    print("\n  N_min table (regenerative payload):")
    header = f"  {'Orbit':<14}" + "".join(f"{'SCS '+str(s)+' kHz':>12}" for s in SCS_LIST)
    print(header)
    print("  " + "-" * (14 + 12 * len(SCS_LIST)))
    for orbit, d in nmin_table.items():
        row = f"  {orbit:<14}"
        for scs in SCS_LIST:
            nm  = d[scs]["n_min"]
            tag = "✗" if nm > MAX_PROC else " "
            row += f"{nm:>10}{tag} "
        print(row)
    print(f"  ✗ = exceeds max {MAX_PROC} processes [TS 38.214, Section 5.1]")

    # ── Bar chart ──────────────────────────────────────────────────────
    fig = plot_nmin_chart(nmin_table, MAX_PROC)
    savefig(fig, "sim03_nmin_chart")

    # ── SE vs N_proc for each orbit ────────────────────────────────────
    N_range = list(range(1, MAX_PROC + 2))
    fig2, axes = plt.subplots(1, 4, figsize=(14, 4), sharey=True)

    orbit_colors = {
        "LEO_600":  COLORS["leo600"],
        "LEO_1200": COLORS["leo1200"],
        "MEO_10000": COLORS["meo"],
        "GEO_35786": COLORS["geo"],
    }

    for ax, (orbit, rtt) in zip(axes, ORBIT_RTT_MS.items()):
        nm_30 = n_min(rtt, 30)
        util_arr = [pipeline_utilization(N, rtt, 30) for N in N_range]

        # SE_GP = util × (1 - BLER_final) × r
        bler_final = 0.05   # approximate at SNR_OP = 5 dB, QPSK r=1/2
        r          = IR_CFG.code_rate
        se_arr     = [u * (1 - bler_final) * r for u in util_arr]

        ax.plot(N_range, se_arr,
                color=orbit_colors[orbit], lw=2, marker="o", ms=4)
        ax.axvline(nm_30, color="red", lw=1.2, ls="--",
                   label=f"$N_{{min}}={nm_30}$")
        ax.axvline(MAX_PROC, color="orange", lw=1.0, ls=":",
                   label=f"Max={MAX_PROC}")
        ax.set_xlabel("N (HARQ processes)")
        ax.set_title(orbit.replace("_", "\n"), fontsize=9)
        ax.grid(True, alpha=0.4)
        ax.legend(fontsize=7)

    axes[0].set_ylabel("SE Goodput [bit/s/Hz]")
    fig2.suptitle("SE Goodput vs N_processes per Orbit  [SCS 30 kHz, $K=15$ dB]",
                  fontsize=11)
    fig2.tight_layout()
    savefig(fig2, "sim03_se_vs_nproc")

    # ── Save data ──────────────────────────────────────────────────────
    out = Path(__file__).parents[2] / "results" / "data"
    flat = {}
    for orbit, d in nmin_table.items():
        for scs, vals in d.items():
            flat[f"{orbit}_scs{scs}_nmin"]     = vals["n_min"]
            flat[f"{orbit}_scs{scs}_feasible"]  = vals["feasible"]
    np.savez(out / "sim03_nmin.npz", **flat)
    print("  Data saved → results/data/sim03_nmin.npz")
    print("  Sim 3 complete.")


if __name__ == "__main__":
    run()
