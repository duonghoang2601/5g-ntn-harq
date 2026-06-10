"""
run_all.py — Master runner for all 5G NTN HARQ simulations.

Usage:
    python run_all.py           # run all 5 simulations
    python run_all.py 1 3 5     # run specific simulations only

Output:
    results/figures/  ← PDF + PNG plots
    results/data/     ← .npz data files
"""

import sys
import time
import traceback
from pathlib import Path


def _ensure_dirs():
    for d in ["results/figures", "results/data"]:
        Path(d).mkdir(parents=True, exist_ok=True)


SIMS = {
    1: ("BLER vs Es/N0",                  "src.sim.sim_01_bler_vs_snr"),
    2: ("SE Goodput vs RTT",              "src.sim.sim_02_throughput_vs_rtt"),
    3: ("N_min Optimisation",             "src.sim.sim_03_nmin"),
    4: ("GEO HARQ-Disable Trade-off",     "src.sim.sim_04_geo_disable"),
    5: ("Energy Efficiency per Bit",      "src.sim.sim_05_energy"),
}


def run_sim(sim_id: int) -> bool:
    label, module = SIMS[sim_id]
    print(f"\n{'#'*62}")
    print(f"#  Simulation {sim_id}: {label}")
    print(f"{'#'*62}")
    t0 = time.time()
    try:
        import importlib
        mod = importlib.import_module(module)
        if sim_id == 1:
            from src.harq.bler_model import MCS_A, MCS_B
            mod.run(MCS_A, "MCS A — QPSK r=1/2",   "mcs_a")
            mod.run(MCS_B, "MCS B — 256QAM r=8/9", "mcs_b")
            print("\nSim 1 complete.")
        else:
            mod.run()
        elapsed = time.time() - t0
        print(f"\n  ✔  Simulation {sim_id} finished in {elapsed:.1f} s")
        return True
    except Exception:
        print(f"\n  ✘  Simulation {sim_id} FAILED:")
        traceback.print_exc()
        return False


def main():
    _ensure_dirs()

    if len(sys.argv) > 1:
        ids = [int(x) for x in sys.argv[1:] if x.isdigit() and 1 <= int(x) <= 5]
    else:
        ids = list(SIMS.keys())

    print("=" * 62)
    print("  5G NTN HARQ — Simulation Suite")
    print(f"  Running: {ids}")
    print("=" * 62)

    t_start = time.time()
    results = {}
    for sid in ids:
        results[sid] = run_sim(sid)

    total = time.time() - t_start
    print(f"\n{'='*62}")
    print(f"  Summary  ({total:.1f} s total)")
    print(f"{'='*62}")
    for sid, ok in results.items():
        status = "✔ OK" if ok else "✘ FAILED"
        print(f"  Sim {sid}: {SIMS[sid][0]:<38}  {status}")

    n_fail = sum(1 for ok in results.values() if not ok)
    if n_fail:
        print(f"\n  {n_fail} simulation(s) failed. Check output above.")
        sys.exit(1)
    else:
        print(f"\n  All simulations passed.")
        print(f"  Figures → results/figures/")
        print(f"  Data    → results/data/")


if __name__ == "__main__":
    main()
