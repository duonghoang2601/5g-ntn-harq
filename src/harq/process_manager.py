"""
HARQ Process Manager — N-process Stop-and-Wait scheduler with RTT model.

Implements the N-process parallel HARQ pipeline. Tracks pipeline stall,
throughput, and latency for any (N, RTT, T_slot) configuration.

Formula: N_min = ceil(2*Tp / T_slot) + 1
Reference: Tuninato 2025, Section IV.A
           TR 38.821, Section 6.4.2
           TS 38.214, Section 5.1 (max 16/32 processes)
"""

import numpy as np
from dataclasses import dataclass
from typing import Literal

from src.channel.lms_channel import ORBIT_RTT_MS
from src.harq.bler_model import TSLOT_MS, simulate_harq_bler, HARQConfig


@dataclass
class SchedulerConfig:
    n_processes: int      # number of parallel HARQ processes
    rtt_ms: float         # round-trip time [ms]  (= 2 * T_propagation)
    scs_khz: int = 30     # subcarrier spacing [kHz]
    max_tx: int = 4       # max transmissions per process


def n_min(rtt_ms: float, scs_khz: int = 30) -> int:
    """
    Minimum HARQ processes to avoid pipeline stall.
    N_min = ceil(2*Tp / T_slot) + 1  [Tuninato 2025, Section IV.A]
    Note: RTT = 2*Tp, so N_min = ceil(RTT / T_slot) + 1
    """
    T_slot = TSLOT_MS[scs_khz]
    return int(np.ceil(rtt_ms / T_slot)) + 1


def pipeline_utilization(n_processes: int, rtt_ms: float,
                         scs_khz: int = 30) -> float:
    """
    Fraction of slots where at least one process is transmitting.
    = min(1,  N / N_min)
    """
    n_m = n_min(rtt_ms, scs_khz)
    return min(1.0, n_processes / n_m)


def simulate_throughput_vs_rtt(
    snr_db: float,
    ch_config,
    harq_config: HARQConfig,
    rtt_values_ms: np.ndarray,
    n_processes_list: list[int],
    scs_khz: int = 30,
    n_trials: int = 15_000,
    seed: int = 0,
) -> dict:
    """
    Compute spectral efficiency (goodput-based SE) vs RTT for several
    values of N_processes.

    SE_GP = utilization × (1 − BLER_final) × SE_nominal
          [Tuninato 2025, Eq. (2)]

    Returns dict keyed by n_processes with arrays of SE_GP vs RTT.
    """
    # BLER at this SNR (independent of RTT for link-level model)
    snr_arr  = np.array([snr_db])
    bler_res = simulate_harq_bler(snr_arr, ch_config, harq_config,
                                   n_trials=n_trials, seed=seed)
    bler_fin = float(bler_res["bler_final"][0])

    r = harq_config.code_rate
    # SE_nominal: bits / channel use = log2(M) * r  (no retransmission)
    # Here we use r as SE_nominal proxy (normalised to 1 Hz, 1 slot)
    se_nominal = r  # [bits/s/Hz] per slot, normalised

    out = {}
    for N in n_processes_list:
        se_list = []
        for rtt in rtt_values_ms:
            util = pipeline_utilization(N, rtt, scs_khz)
            se   = util * (1 - bler_fin) * se_nominal
            se_list.append(se)
        out[N] = np.array(se_list)

    return out


def simulate_nmin_table(
    scs_list: list[int] = (15, 30, 60, 120),
    max_proc: int = 32,
) -> dict:
    """
    Compute N_min for each orbit × SCS combination.
    Returns dict: orbit → {scs: N_min}
    Also flags which cases exceed max_proc (i.e., pipeline stall inevitable).

    Reference: Tuninato 2025, Table 5; TS 38.214 Section 5.1 (max 32)
    """
    result = {}
    for orbit, rtt in ORBIT_RTT_MS.items():
        result[orbit] = {}
        for scs in scs_list:
            nm = n_min(rtt, scs)
            result[orbit][scs] = {
                "n_min": nm,
                "feasible": nm <= max_proc,
                "rtt_ms": rtt,
            }
    return result


def simulate_geo_disable_comparison(
    snr_db_range: np.ndarray,
    ch_config,
    harq_config_harq: HARQConfig,
    n_proc_harq: int = 32,
    n_proc_rlc: int = 32,
    rlc_max_tx: int = 32,
    scs_khz: int = 30,
    n_trials: int = 15_000,
    seed: int = 1,
) -> dict:
    """
    GEO scenario: compare HARQ (with large N) vs HARQ-disabled (RLC ARQ).

    HARQ mode (Solution 1 of TR 38.821 Section 6.4.2):
      - Use N_proc_harq processes, accept pipeline stall if N < N_min
      - Utilization = min(1, N/N_min)

    RLC ARQ mode (Solution 2 / TR 38.821 Section 6.4.1):
      - No HARQ combining — RLC retransmits whole TB, no soft combining
      - Modelled as: same BLER per TX attempt (memoryless, no combining)
      - RLC RTT ≈ 2 × HARQ RTT (RLC layer overhead)

    Returns: {'harq': {...}, 'rlc': {...}} with bler, se_gp, latency arrays
    """
    rtt_geo   = ORBIT_RTT_MS["GEO_35786"]
    T_slot    = TSLOT_MS[scs_khz]
    util_harq = pipeline_utilization(n_proc_harq, rtt_geo, scs_khz)
    r         = harq_config_harq.code_rate
    se_nom    = r

    # HARQ simulation (IR combining)
    harq_res  = simulate_harq_bler(snr_db_range, ch_config, harq_config_harq,
                                    n_trials=n_trials, seed=seed)
    bler_harq = harq_res["bler_final"]
    ntx_harq  = harq_res["avg_ntx"]
    se_harq   = util_harq * (1 - bler_harq) * se_nom
    lat_harq  = ntx_harq * (T_slot + rtt_geo)

    # RLC ARQ simulation (no combining, memoryless)
    # After k attempts: residual BLER = bler_1tx^k  (independent errors)
    # We model bler_1tx as no-HARQ BLER
    from src.harq.bler_model import no_harq_bler
    bler_1tx  = no_harq_bler(snr_db_range, ch_config, r,
                              n_trials=n_trials, seed=seed+1)
    # Residual BLER after rlc_max_tx attempts
    bler_rlc  = bler_1tx ** rlc_max_tx
    # Average TX count for RLC (geometric series)
    p         = np.clip(1 - bler_1tx, 1e-9, 1.0)
    ntx_rlc   = np.minimum(1 / p, rlc_max_tx)
    # RLC RTT is larger (includes RLC processing overhead)
    rtt_rlc   = 2 * rtt_geo
    se_rlc    = (1 - bler_rlc) * se_nom
    lat_rlc   = ntx_rlc * (T_slot + rtt_rlc)

    return {
        "harq": {"bler": bler_harq, "se_gp": se_harq, "latency": lat_harq,
                 "avg_ntx": ntx_harq, "utilization": util_harq},
        "rlc":  {"bler": bler_rlc,  "se_gp": se_rlc,  "latency": lat_rlc,
                 "avg_ntx": ntx_rlc},
    }


def simulate_energy_per_bit(
    snr_db_range: np.ndarray,
    ch_config,
    harq_configs: dict[str, HARQConfig],
    orbit_rtts: dict[str, float] | None = None,
    n_trials: int = 15_000,
    seed: int = 2,
) -> dict:
    """
    Energy per successfully delivered bit [normalised, P_tx = 1 W].

    E_bit = P_tx * avg_ntx * T_slot / (k * (1 - BLER_final))
    [See: 09_evaluation_criteria.md]

    Returns nested dict: scheme → array of E_bit vs SNR
    """
    if orbit_rtts is None:
        orbit_rtts = ORBIT_RTT_MS

    T_slot = TSLOT_MS[30] * 1e-3  # [s]
    k_norm = 1.0                   # normalised information bits
    P_tx   = 1.0                   # normalised transmit power

    results = {}
    for name, hcfg in harq_configs.items():
        res     = simulate_harq_bler(snr_db_range, ch_config, hcfg,
                                      n_trials=n_trials, seed=seed)
        ntx     = res["avg_ntx"]
        bler_f  = np.clip(res["bler_final"], 0, 1 - 1e-9)
        # energy per bit (normalised)
        e_bit   = P_tx * ntx * T_slot / (k_norm * (1 - bler_f))
        results[name] = {"e_bit": e_bit, "avg_ntx": ntx, "bler": bler_f}

    return results
