"""
Simulation 4 — GEO HARQ-Disable Trade-off

Compares two 3GPP Rel-17 solutions for GEO (RTT ≈ 270 ms regenerative):
  Solution 1: HARQ-IR with N=32 processes (pipeline partially stalled)
  Solution 2: HARQ feedback disabled, rely on RLC ARQ (no soft combining)

Metrics: BLER, SE Goodput, Latency

Reference: TR 38.821, Section 6.4.1 (HARQ disable)
           TR 38.821, Section 6.4.2 (HARQ process count increase)
           Tuninato 2025, Section III.B (RLC ARQ as memoryless)
           TR 38.811, Table 5.3.2.1-1 (GEO RTT = 270 ms regenerative)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

import numpy as np

from src.channel.lms_channel import ChannelConfig
from src.harq.bler_model import HARQConfig
from src.harq.process_manager import simulate_geo_disable_comparison
from src.plots.plot_utils import plot_geo_disable, savefig

SNR_DB   = np.arange(-5, 22, 0.5)
N_TRIALS = 25_000

# Channel: K=15 dB, 50 km/h, Ka-band (Tuninato 2025, Section IV)
CH = ChannelConfig(K_dB=15.0, speed_kmh=50.0, fc_GHz=20.0)

# HARQ config: MCS A (QPSK r=1/2) for GEO worst-case
GEO_HARQ_CFG = HARQConfig(code_rate=1/2, max_retx=3, scheme="IR")


def run() -> None:
    print("\n" + "="*60)
    print("  Sim 4 — GEO HARQ-Disable Trade-off")
    print("="*60)
    print("  GEO RTT = 270.6 ms (regenerative, 10° elevation)")
    print("  [TR 38.811, Table 5.3.2.1-1]")
    print("  N_min at SCS 30 kHz = 542 → stall inevitable with N=32")
    print()

    results = simulate_geo_disable_comparison(
        snr_db_range=SNR_DB,
        ch_config=CH,
        harq_config_harq=GEO_HARQ_CFG,
        n_proc_harq=32,
        rlc_max_tx=32,
        scs_khz=30,
        n_trials=N_TRIALS,
        seed=99,
    )

    fig = plot_geo_disable(SNR_DB, results)
    savefig(fig, "sim04_geo_disable")

    # Print key comparison
    snr_ref = 10.0
    idx = np.argmin(np.abs(SNR_DB - snr_ref))
    print(f"\n  At Es/N0 = {snr_ref} dB:")
    print(f"    HARQ (N=32):    BLER={results['harq']['bler'][idx]:.2e}  "
          f"SE={results['harq']['se_gp'][idx]:.4f}  "
          f"Latency={results['harq']['latency'][idx]:.0f} ms  "
          f"(util={results['harq']['utilization']:.3f})")
    print(f"    RLC ARQ:        BLER={results['rlc']['bler'][idx]:.2e}  "
          f"SE={results['rlc']['se_gp'][idx]:.4f}  "
          f"Latency={results['rlc']['latency'][idx]:.0f} ms")

    out = Path(__file__).parents[2] / "results" / "data"
    np.savez(out / "sim04_geo_disable.npz",
             snr_db=SNR_DB,
             harq_bler=results["harq"]["bler"],
             harq_se=results["harq"]["se_gp"],
             harq_latency=results["harq"]["latency"],
             rlc_bler=results["rlc"]["bler"],
             rlc_se=results["rlc"]["se_gp"],
             rlc_latency=results["rlc"]["latency"])
    print("  Data saved → results/data/sim04_geo_disable.npz")
    print("  Sim 4 complete.")


if __name__ == "__main__":
    run()
