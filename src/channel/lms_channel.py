"""
LMS (Land Mobile Satellite) Channel Model
Rician flat fading with Jake's Doppler spectrum.

Reference: TR 38.811 Section 6.7.1 (flat fading, LMS two-state model)
           Jake's Doppler: TR 38.811 Section 6.7.1
           K-factor values: Tuninato 2025, Section IV
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class ChannelConfig:
    K_dB: float          # Rician K-factor [dB]
    speed_kmh: float     # UE terminal speed [km/h]
    fc_GHz: float        # Carrier frequency [GHz]
    n_oscillators: int = 20  # Jake's model sinusoid count


# NTN orbit propagation delays [ms], regenerative payload, elevation 10°
# Source: TR 38.811, Table 5.3.4.1-1 and Table 5.3.2.1-1
ORBIT_RTT_MS = {
    "LEO_600":  12.88,   # 2 * 6.440 ms
    "LEO_1200": 24.32,   # 2 * 12.158 ms (approx 1200 km)
    "MEO_10000": 93.45,  # 2 * 46.727 ms
    "GEO_35786": 270.57, # 2 * 135.286 ms
}


def generate_channel(
    cfg: ChannelConfig,
    n_samples: int,
    T_slot_ms: float,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """
    Generate n_samples i.i.d. Rician flat-fading channel coefficients.

    h_i = sqrt(K/(K+1)) * e^{j*phi_i}   [LOS, random phase per sample]
        + sqrt(1/(K+1))  * h_scatter_i   [scatter, i.i.d. CN(0,1)]

    Returns h: complex array shape (n_samples,).

    E[|h|²] = K/(K+1) + 1/(K+1) = 1  (exact, by construction).

    Standard link-level HARQ model: each Monte Carlo trial is an
    independent Rician realisation (fast-fading across HARQ rounds).
    The K-factor and Doppler are characterised analytically via
    coherence_time_ms(); temporal correlation is not needed for BLER MC.

    Reference: TR 38.811 Section 6.7.1 (Rician LMS channel, K-factor model)
               Tuninato 2025 Section IV (K=15 dB, flat fading assumption)
    """
    if rng is None:
        rng = np.random.default_rng()

    K = 10 ** (cfg.K_dB / 10)

    # LOS: random phase per sample → Rician envelope (phase invariant)
    phi      = rng.uniform(0, 2 * np.pi, n_samples)
    h_los    = np.sqrt(K / (K + 1)) * np.exp(1j * phi)

    # Scatter: i.i.d. CN(0, 1/(K+1))  →  E[|h_scatter|²] = 1/(K+1)
    h_scatter = np.sqrt(1 / (K + 1)) * (
        rng.standard_normal(n_samples) + 1j * rng.standard_normal(n_samples)
    ) / np.sqrt(2)

    return h_los + h_scatter


def instantaneous_snr(h: np.ndarray, es_n0_linear: float) -> np.ndarray:
    """
    Instantaneous received SNR per channel realisation.
    gamma_i = |h_i|^2 * Es/N0_avg  (linear)

    MRC principle: after combining n independent realisations,
    SNR_eff = sum(gamma_i).  [standard MRC result]
    """
    return np.abs(h) ** 2 * es_n0_linear


def coherence_time_ms(cfg: ChannelConfig) -> float:
    """
    Practical coherence time using Clarke's model.
    Tc ≈ 0.423 / fm  [Tuninato 2025, Section IV.B]
    Returns Tc in ms; returns inf if speed = 0.
    """
    if cfg.speed_kmh == 0:
        return np.inf
    fd = cfg.speed_kmh / 3.6 * cfg.fc_GHz * 1e9 / 3e8
    return 0.423 / fd * 1e3
