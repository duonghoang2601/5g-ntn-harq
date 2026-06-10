"""
Simulation 5 — Energy Efficiency per Successfully Delivered Bit

E_bit = P_tx · avg_ntx · T_slot / (k · (1 − BLER_final))   [normalised]

Compares: No HARQ / CC-HARQ / IR-HARQ
Also compares across orbits (LEO 600, MEO, GEO) for IR-HARQ.

This is an original contribution of the project (not in Tuninato 2025).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

import numpy as np
import matplotlib.pyplot as plt

from src.channel.lms_channel import ChannelConfig, ORBIT_RTT_MS
from src.harq.bler_model import HARQConfig, no_harq_bler, simulate_harq_bler, TSLOT_MS
from src.harq.process_manager import simulate_energy_per_bit, pipeline_utilization
from src.plots.plot_utils import plot_energy_per_bit, savefig, COLORS, LINESTYLES, MARKERS

SNR_DB   = np.arange(-10, 25, 0.5)
N_TRIALS = 25_000
CH       = ChannelConfig(K_dB=15.0, speed_kmh=50.0, fc_GHz=20.0)

HARQ_CFGS = {
    "No HARQ":  HARQConfig(code_rate=1/2, max_retx=0, scheme="IR"),
    "CC-HARQ":  HARQConfig(code_rate=1/2, max_retx=3, scheme="CC"),
    "IR-HARQ":  HARQConfig(code_rate=1/2, max_retx=3, scheme="IR"),
}


def run() -> None:
    print("\n" + "="*60)
    print("  Sim 5 — Energy Efficiency per Bit")
    print("="*60)

    # ── Part A: No HARQ vs CC vs IR at LEO 600 km ─────────────────────
    print("  [A] No HARQ / CC-HARQ / IR-HARQ — LEO 600 km …")
    energy_res = simulate_energy_per_bit(SNR_DB, CH, HARQ_CFGS,
                                          n_trials=N_TRIALS, seed=77)

    fig = plot_energy_per_bit(SNR_DB, energy_res)
    savefig(fig, "sim05_energy_per_bit")

    # ── Part B: IR-HARQ across orbits ─────────────────────────────────
    print("  [B] IR-HARQ across orbits …")
    ir_cfg   = HARQConfig(code_rate=1/2, max_retx=3, scheme="IR")
    res_ir   = simulate_harq_bler(SNR_DB, CH, ir_cfg,
                                   n_trials=N_TRIALS, seed=88)
    T_slot   = TSLOT_MS[30] * 1e-3  # [s]
    P_tx     = 1.0

    fig2, ax = plt.subplots(figsize=(7, 4.5))

    orbit_colors = {
        "LEO_600":   COLORS["leo600"],
        "LEO_1200":  COLORS["leo1200"],
        "MEO_10000": COLORS["meo"],
        "GEO_35786": COLORS["geo"],
    }

    for idx, (orbit, rtt) in enumerate(ORBIT_RTT_MS.items()):
        util  = pipeline_utilization(n_processes=32, rtt_ms=rtt, scs_khz=30)
        ntx   = res_ir["avg_ntx"]
        bler  = np.clip(res_ir["bler_final"], 0, 1 - 1e-9)
        # Energy per bit accounts for pipeline stall (effective throughput reduced)
        # More idle time → more energy wasted per delivered bit
        e_bit = P_tx * ntx * T_slot / (max(util, 1e-3) * (1 - bler))
        ax.semilogy(SNR_DB, e_bit,
                    color=orbit_colors[orbit],
                    ls=LINESTYLES[idx], marker=MARKERS[idx], markevery=5,
                    label=orbit.replace("_", " "))

    ax.set_xlabel(r"$E_s/N_0$ [dB]")
    ax.set_ylabel("Normalised Energy per Bit [J/bit]")
    ax.set_title("Energy Efficiency — IR-HARQ across Orbits\n"
                 "[$N=32$, SCS 30 kHz, MCS A, $K=15$ dB]")
    ax.legend()
    ax.grid(True)
    fig2.tight_layout()
    savefig(fig2, "sim05_energy_per_bit_orbits")

    # ── Summary table ─────────────────────────────────────────────────
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
             **{f"{name.replace(' ','_')}_ebit": res["e_bit"]
                for name, res in energy_res.items()})
    print("  Data saved → results/data/sim05_energy.npz")
    print("  Sim 5 complete.")


if __name__ == "__main__":
    run()
