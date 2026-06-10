"""
Simulation 1 — BLER vs Es/N0

Compares: No HARQ / CC-HARQ / IR-HARQ
Channel : LMS Rician K=15 dB, speed=50 km/h, LEO 600 km
MCS     : A (QPSK r=1/2)  and  B (256QAM r=8/9)

Reference: Tuninato 2025, Section V.C, Fig. 6 & 7
           TR 38.811 Section 6.7.1 (channel model)
           TS 38.212 Table 5.4.2.1-2 (RV sequence)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

import numpy as np
from tqdm import tqdm

from src.channel.lms_channel import ChannelConfig
from src.harq.bler_model import (
    HARQConfig, simulate_harq_bler, no_harq_bler, MCS_A, MCS_B
)
from src.plots.plot_utils import plot_bler_vs_snr, savefig

import numpy as np

SNR_DB   = np.arange(-10, 25, 0.5)
N_TRIALS = 30_000

# Channel: K=15 dB, 50 km/h, Ka-band 20 GHz (Tuninato 2025, Section IV)
CH = ChannelConfig(K_dB=15.0, speed_kmh=50.0, fc_GHz=20.0)


def run(mcs: HARQConfig, mcs_label: str, tag: str) -> None:
    print(f"\n{'='*60}")
    print(f"  Sim 1 — {mcs_label}")
    print(f"{'='*60}")

    cc_cfg = HARQConfig(code_rate=mcs.code_rate, max_retx=mcs.max_retx,
                        scheme="CC")
    ir_cfg = HARQConfig(code_rate=mcs.code_rate, max_retx=mcs.max_retx,
                        scheme="IR")

    print("  [1/3] No HARQ baseline …")
    bler_none = no_harq_bler(SNR_DB, CH, mcs.code_rate,
                              n_trials=N_TRIALS, seed=10)

    print("  [2/3] CC-HARQ …")
    bler_cc   = simulate_harq_bler(SNR_DB, CH, cc_cfg,
                                    n_trials=N_TRIALS, seed=20)

    print("  [3/3] IR-HARQ …")
    bler_ir   = simulate_harq_bler(SNR_DB, CH, ir_cfg,
                                    n_trials=N_TRIALS, seed=30)

    fig = plot_bler_vs_snr(SNR_DB, bler_none, bler_cc, bler_ir,
                            mcs_label=mcs_label, K_dB=15.0)
    savefig(fig, f"sim01_bler_vs_snr_{tag}")

    # Print HARQ gain at BLER=1e-2
    target_bler = 1e-2
    for label, bler_d in [("CC", bler_cc), ("IR", bler_ir)]:
        for tx in range(1, mcs.max_retx + 2):
            key  = f"bler_tx{tx}"
            vals = bler_d[key]
            if vals.min() < target_bler:
                snr_thr = np.interp(target_bler, vals[::-1], SNR_DB[::-1])
                print(f"  {label} TX={tx}: BLER={target_bler:.0e} at "
                      f"Es/N0={snr_thr:.1f} dB")

    # Save data
    out_dir = Path(__file__).parents[2] / "results" / "data"
    np.savez(out_dir / f"sim01_{tag}.npz",
             snr_db=SNR_DB,
             bler_no_harq=bler_none,
             **{f"cc_{k}": v for k, v in bler_cc.items()},
             **{f"ir_{k}": v for k, v in bler_ir.items()})
    print(f"  Data saved → results/data/sim01_{tag}.npz")


if __name__ == "__main__":
    run(MCS_A, "MCS A — QPSK r=1/2",   "mcs_a")
    run(MCS_B, "MCS B — 256QAM r=8/9", "mcs_b")
    print("\nSim 1 complete.")
