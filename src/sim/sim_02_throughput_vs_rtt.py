"""
Simulation 2 — Spectral Efficiency (Goodput) vs RTT

Shows how throughput degrades as RTT increases (LEO → MEO → GEO) for
different numbers of HARQ processes, illustrating the pipeline stall effect.

SE_GP = utilization × (1 − BLER_final) × SE_nominal   [Tuninato 2025, Eq.(2)]
utilization = min(1, N / N_min)                         [Tuninato 2025, IV.A]

Reference: TR 38.811, Tables 5.3.4.1-1 and 5.3.2.1-1 (RTT values)
           TS 38.214, Section 5.1 (max 16 / 32 processes)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

import numpy as np

from src.channel.lms_channel import ChannelConfig, ORBIT_RTT_MS
from src.harq.bler_model import HARQConfig, MCS_A
from src.harq.process_manager import simulate_throughput_vs_rtt, n_min
from src.plots.plot_utils import plot_throughput_vs_rtt, savefig, COLORS

import matplotlib.pyplot as plt

N_TRIALS = 20_000
SNR_OP   = 5.0      # operating point [dB] — above QPSK r=1/2 waterfall
CH       = ChannelConfig(K_dB=15.0, speed_kmh=50.0, fc_GHz=20.0)
IR_CFG   = HARQConfig(code_rate=1/2, max_retx=3, scheme="IR")

RTT_SWEEP = np.concatenate([
    np.linspace(5,  60,  30),   # LEO range
    np.linspace(60, 200, 20),   # MEO range
    np.linspace(200, 600, 20),  # GEO range
])

N_PROC_LIST = [4, 8, 16, 32]


def run() -> None:
    print("\n" + "="*60)
    print("  Sim 2 — SE Goodput vs RTT")
    print("="*60)

    se_by_n = simulate_throughput_vs_rtt(
        snr_db=SNR_OP,
        ch_config=CH,
        harq_config=IR_CFG,
        rtt_values_ms=RTT_SWEEP,
        n_processes_list=N_PROC_LIST,
        scs_khz=30,
        n_trials=N_TRIALS,
        seed=42,
    )

    fig = plot_throughput_vs_rtt(RTT_SWEEP, se_by_n, ORBIT_RTT_MS,
                                  scheme="IR-HARQ")
    savefig(fig, "sim02_throughput_vs_rtt")

    # Extra: show N_min thresholds on a separate plot
    fig2, ax = plt.subplots(figsize=(8, 4))
    colors = list(COLORS.values())
    for idx, (N, se) in enumerate(se_by_n.items()):
        ax.plot(RTT_SWEEP, se, color=colors[idx+1],
                label=f"N={N}", linewidth=2)

    for orbit, rtt in ORBIT_RTT_MS.items():
        nm = n_min(rtt, scs_khz=30)
        ax.axvline(rtt, color="gray", lw=0.8, ls="--", alpha=0.5)
        ax.text(rtt+3, 0.01, f"{orbit.replace('_','\\n')}\n$N_{{min}}$={nm}",
                fontsize=7, color="gray")

    ax.set_xlim(0, 620)
    ax.set_xlabel("RTT [ms]  (2 × propagation delay, regenerative payload)")
    ax.set_ylabel("SE Goodput [bit/s/Hz]")
    ax.set_title("Throughput Collapse vs RTT for Different HARQ Process Counts\n"
                 "[SCS 30 kHz, MCS A, IR-HARQ, $K=15$ dB, $E_s/N_0=5$ dB]")
    ax.legend()
    ax.grid(True)
    fig2.tight_layout()
    savefig(fig2, "sim02_throughput_vs_rtt_annotated")

    out = Path(__file__).parents[2] / "results" / "data"
    np.savez(out / "sim02.npz",
             rtt_ms=RTT_SWEEP,
             **{f"se_N{N}": v for N, v in se_by_n.items()})
    print("  Data saved → results/data/sim02.npz")
    print("  Sim 2 complete.")


if __name__ == "__main__":
    run()
