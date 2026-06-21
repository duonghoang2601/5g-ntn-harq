"""
Simulation 1 — BLER vs Es/N0  (IR-HARQ only, MCS A, LEO 600 km)

Compares: No HARQ  vs  IR-HARQ (TX = 1..4)
Channel : LMS Rician K=15 dB, speed=50 km/h, LEO 600 km
MCS     : A (QPSK r=1/2)

Reference: Tuninato 2025, Section V.C, Fig. 6
           TR 38.811 Section 6.7.1 (channel model)
           TS 38.212 Table 5.4.2.1-2 (RV sequence)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

import numpy as np
from tqdm import tqdm

from src.channel.lms_channel import ChannelConfig
from src.harq.bler_model import HARQConfig, simulate_harq_bler, no_harq_bler, MCS_A
from src.plots.plot_utils import savefig

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SNR_DB   = np.arange(-12, 8.5, 0.5)
N_TRIALS = 20_000

# Channel: K=15 dB, 50 km/h, Ka-band DL 20 GHz (Tuninato 2025, Table 4)
CH = ChannelConfig(K_dB=15.0, speed_kmh=50.0, fc_GHz=20.0)


def run() -> None:
    mcs = MCS_A
    print("\n" + "=" * 60)
    print("  Sim 1 — BLER vs Es/N0  [IR-HARQ, MCS A, LEO 600 km]")
    print("=" * 60)

    ir_cfg = HARQConfig(code_rate=mcs.code_rate, max_retx=mcs.max_retx, scheme="IR")

    print("  [1/2] No HARQ baseline …")
    bler_none = no_harq_bler(SNR_DB, CH, mcs.code_rate, n_trials=N_TRIALS, seed=10)

    print("  [2/2] IR-HARQ …")
    bler_ir = simulate_harq_bler(SNR_DB, CH, ir_cfg, n_trials=N_TRIALS, seed=30)

    # ── Plot ────────────────────────────────────────────────────────────
    ir_shades = plt.cm.Blues(np.linspace(0.35, 0.90, mcs.max_retx + 1))
    markers   = ["o", "s", "^", "D"]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.semilogy(SNR_DB, np.clip(bler_none, 1e-7, 1.0),
                color="#888888", ls=":", lw=1.5, marker="x", markevery=6,
                label="No HARQ")

    for tx in range(1, mcs.max_retx + 2):
        ax.semilogy(SNR_DB, np.clip(bler_ir[f"bler_tx{tx}"], 1e-7, 1.0),
                    color=ir_shades[tx - 1], lw=1.8,
                    marker=markers[(tx - 1) % 4], markevery=6,
                    label=f"IR TX = {tx}")

    ax.axhline(1e-3, color="gray", lw=0.7, ls="--", alpha=0.6,
               label=r"Target BLER $10^{-3}$")
    ax.set_xlabel(r"$E_s/N_0$ [dB]")
    ax.set_ylabel("BLER")
    ax.set_ylim(1e-7, 1.05)
    ax.set_title("BLER vs $E_s/N_0$ — IR-HARQ, MCS A (QPSK r=1/2)\n"
                 "K=15 dB, LEO 600 km, SCS 30 kHz")
    ax.legend(fontsize=8.5, loc="upper right")
    ax.grid(True)
    fig.tight_layout()
    savefig(fig, "sim01_bler_ir_leo")

    # ── Print gain at BLER = 1e-3 ───────────────────────────────────────
    target = 1e-3
    for tx in range(1, mcs.max_retx + 2):
        vals = bler_ir[f"bler_tx{tx}"]
        if vals.min() < target:
            snr_thr = np.interp(target, vals[::-1], SNR_DB[::-1])
            print(f"  IR TX={tx}: BLER={target:.0e} at Es/N0={snr_thr:.1f} dB")

    # ── Save data ───────────────────────────────────────────────────────
    out_dir = Path(__file__).parents[2] / "results" / "data"
    save_dict = {"snr_db": SNR_DB, "bler_no_harq": bler_none}
    for tx in range(1, mcs.max_retx + 2):
        save_dict[f"ir_bler_tx{tx}"] = bler_ir[f"bler_tx{tx}"]
    np.savez(out_dir / "sim01_mcs_a.npz", **save_dict)
    print("  Data saved → results/data/sim01_mcs_a.npz")
    print("\nSim 1 complete.")


if __name__ == "__main__":
    run()
