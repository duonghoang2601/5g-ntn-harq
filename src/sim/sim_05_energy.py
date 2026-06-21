"""
Simulation 3 (formerly 5) — Energy Efficiency per Delivered Bit

E_bit = P_tx * avg_ntx * T_slot / (util * (1 - BLER_final))

Compares: No HARQ  vs  IR-HARQ  at LEO 600 km, SCS 30 kHz.

Reference: Tuninato 2025 (energy metric concept)
           TR 38.811, TS 38.214
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.channel.lms_channel import ChannelConfig
from src.harq.bler_model import HARQConfig, no_harq_bler, simulate_harq_bler, TSLOT_MS
from src.harq.process_manager import simulate_energy_per_bit
from src.plots.plot_utils import savefig

SNR_DB   = np.arange(-10, 25, 0.5)
N_TRIALS = 25_000
CH       = ChannelConfig(K_dB=15.0, speed_kmh=50.0, fc_GHz=20.0)

HARQ_CFGS = {
    "No HARQ": HARQConfig(code_rate=1/2, max_retx=0, scheme="IR"),
    "IR-HARQ": HARQConfig(code_rate=1/2, max_retx=3, scheme="IR"),
}


def run() -> None:
    print("\n" + "=" * 60)
    print("  Sim 3 — Energy Efficiency per Bit  [IR-HARQ, LEO 600 km]")
    print("=" * 60)

    energy_res = simulate_energy_per_bit(SNR_DB, CH, HARQ_CFGS,
                                          n_trials=N_TRIALS, seed=77)

    # ── Plot ─────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(7, 4.5))
    styles = {
        "No HARQ": {"color": "#888888", "ls": ":", "marker": "x"},
        "IR-HARQ": {"color": "#1a6fbf", "ls": "-", "marker": "o"},
    }
    for name, res in energy_res.items():
        s = styles[name]
        ax.semilogy(SNR_DB, np.clip(res["e_bit"], 1e-5, 1e7),
                    color=s["color"], ls=s["ls"], lw=1.8,
                    marker=s["marker"], markevery=6, label=name)

    ax.set_xlabel(r"$E_s/N_0$ [dB]")
    ax.set_ylabel(r"$E_{\mathrm{bit}}$ [J/bit]  ($P_{tx}=1$ W, chuẩn hóa)")
    ax.set_ylim(1e-5, 1e7)
    ax.set_title("Năng lượng/bit vs $E_s/N_0$\n"
                 "LEO 600 km, K=15 dB, MCS A, SCS 30 kHz")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, which="both", alpha=0.4)
    fig.tight_layout()
    savefig(fig, "sim05_energy_per_bit")

    # ── Summary ──────────────────────────────────────────────────────────
    snr_ref = 5.0
    idx_ref = np.argmin(np.abs(SNR_DB - snr_ref))
    print(f"\n  Energy comparison at Es/N0 = {snr_ref} dB:")
    for name, res in energy_res.items():
        print(f"    {name:<12}: E_bit={res['e_bit'][idx_ref]:.3e} J/bit  "
              f"avg_ntx={res['avg_ntx'][idx_ref]:.2f}  "
              f"BLER={res['bler'][idx_ref]:.2e}")

    out = Path(__file__).parents[2] / "results" / "data"
    np.savez(out / "sim05_energy.npz",
             snr_db=SNR_DB,
             **{name.replace(" ", "_") + "_ebit": res["e_bit"]
                for name, res in energy_res.items()})
    print("  Data saved → results/data/sim05_energy.npz")
    print("  Sim 3 complete.")


if __name__ == "__main__":
    run()
