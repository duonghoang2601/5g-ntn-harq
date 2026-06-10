"""
Professional plot utilities for 5G NTN HARQ simulation results.
Publication-quality figures with IEEE-style formatting.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

matplotlib.rcParams.update({
    "font.family":       "serif",
    "font.size":         11,
    "axes.titlesize":    12,
    "axes.labelsize":    11,
    "xtick.labelsize":   10,
    "ytick.labelsize":   10,
    "legend.fontsize":   9,
    "legend.framealpha": 0.9,
    "lines.linewidth":   1.8,
    "lines.markersize":  5,
    "grid.alpha":        0.35,
    "grid.linestyle":    "--",
    "figure.dpi":        150,
    "savefig.dpi":       300,
    "savefig.bbox":      "tight",
})

FIGDIR = Path(__file__).parents[2] / "results" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

# Colour palette (colour-blind friendly)
COLORS = {
    "no_harq": "#555555",
    "cc":      "#E74C3C",
    "ir":      "#2980B9",
    "rlc":     "#27AE60",
    "leo600":  "#2980B9",
    "leo1200": "#8E44AD",
    "meo":     "#E67E22",
    "geo":     "#C0392B",
}

LINESTYLES = ["-", "--", "-.", ":", (0, (3, 1, 1, 1))]
MARKERS    = ["o", "s", "^", "D", "v"]


def savefig(fig: plt.Figure, name: str) -> Path:
    path = FIGDIR / f"{name}.pdf"
    fig.savefig(path)
    path_png = FIGDIR / f"{name}.png"
    fig.savefig(path_png)
    print(f"  Saved → {path}")
    return path


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: BLER vs Es/N0
# ─────────────────────────────────────────────────────────────────────────────

def plot_bler_vs_snr(
    snr_db: np.ndarray,
    bler_no_harq: np.ndarray,
    bler_cc: dict,
    bler_ir: dict,
    mcs_label: str = "MCS A (QPSK r=1/2)",
    K_dB: float = 15.0,
) -> plt.Figure:
    """Two-panel figure: (a) CC-HARQ  |  (b) IR-HARQ, both vs No HARQ baseline."""

    max_tx = sum(1 for k in bler_cc if k.startswith("bler_tx"))

    # Colour gradients: darker shade = more transmissions = better combining
    cc_shades = plt.cm.Reds_r(np.linspace(0.05, 0.55, max_tx))
    ir_shades = plt.cm.Blues_r(np.linspace(0.05, 0.55, max_tx))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)

    for ax, shades, scheme, bler_d, panel in [
        (axes[0], cc_shades, "CC-HARQ", bler_cc, "a"),
        (axes[1], ir_shades, "IR-HARQ", bler_ir, "b"),
    ]:
        ax.semilogy(snr_db, bler_no_harq,
                    color="#888888", ls=":", lw=1.5, marker="x", markevery=6,
                    label="No HARQ (baseline)")
        for tx in range(1, max_tx + 1):
            ax.semilogy(snr_db, bler_d[f"bler_tx{tx}"],
                        color=shades[tx - 1], lw=1.8,
                        marker=MARKERS[tx - 1], markevery=6,
                        label=f"TX = {tx}")
        ax.axhline(1e-3, color="gray", lw=0.7, ls="--", alpha=0.6,
                   label=r"Target BLER $10^{-3}$")
        ax.set_xlabel(r"$E_s/N_0$ [dB]")
        ax.set_title(f"({panel}) {scheme}")
        ax.set_ylim(1e-5, 1.05)
        ax.legend(fontsize=8.5, loc="lower left")
        ax.grid(True)

    axes[0].set_ylabel("BLER")
    fig.suptitle(
        f"BLER vs $E_s/N_0$ — {mcs_label},  $K = {K_dB}$ dB,  LEO 600 km",
        fontsize=12,
    )
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: Throughput (SE_GP) vs RTT
# ─────────────────────────────────────────────────────────────────────────────

def plot_throughput_vs_rtt(
    rtt_ms: np.ndarray,
    se_by_n: dict,        # {N_proc: se_array}
    orbit_rtts: dict,     # orbit label → rtt value
    scheme: str = "IR-HARQ",
) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(6.5, 4.2))

    for idx, (N, se) in enumerate(se_by_n.items()):
        ax.plot(rtt_ms, se,
                color=list(COLORS.values())[idx + 1],
                ls=LINESTYLES[idx], marker=MARKERS[idx], markevery=3,
                label=f"$N={N}$ processes")

    # Mark orbit RTT positions — stagger label heights to prevent overlap
    ylo, yhi = ax.get_ylim()
    y_fracs = [0.92, 0.72, 0.52, 0.32]   # LEO_600 → GEO (decreasing)
    for i, (orbit, rtt) in enumerate(orbit_rtts.items()):
        ax.axvline(rtt, color="gray", lw=0.7, ls="--", alpha=0.6)
        y_pos = ylo + (yhi - ylo) * y_fracs[i]
        ax.text(rtt + 2, y_pos, orbit.replace("_", "\n"),
                fontsize=7, color="gray", va="top")

    ax.set_xlabel("RTT [ms]")
    ax.set_ylabel("Spectral Efficiency (Goodput) [bit/s/Hz]")
    ax.set_title(f"SE Goodput vs RTT — {scheme}")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3: N_min heatmap / bar chart
# ─────────────────────────────────────────────────────────────────────────────

def plot_nmin_chart(nmin_table: dict, max_proc: int = 32) -> plt.Figure:
    """
    Grouped bar chart of N_min per orbit and SCS.
    """
    orbits  = list(nmin_table.keys())
    scs_all = sorted({s for v in nmin_table.values() for s in v.keys()})

    x     = np.arange(len(orbits))
    width = 0.18

    fig, ax = plt.subplots(figsize=(8, 4.5))

    for i, scs in enumerate(scs_all):
        vals = [nmin_table[o][scs]["n_min"] for o in orbits]
        bars = ax.bar(x + i * width, vals, width,
                      label=f"SCS {scs} kHz",
                      color=list(COLORS.values())[i],
                      alpha=0.85)
        # Mark infeasible (> max_proc)
        for bar, v in zip(bars, vals):
            if v > max_proc:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        min(v, ax.get_ylim()[1]) + 1,
                        f"{v}", ha="center", va="bottom",
                        fontsize=7, color="red", fontweight="bold")

    ax.axhline(max_proc, color="red", lw=1.2, ls="--",
               label=f"Max processes = {max_proc} [TS 38.214]")
    ax.set_xticks(x + width * (len(scs_all) - 1) / 2)
    ax.set_xticklabels([o.replace("_", "\n") for o in orbits])
    ax.set_ylabel("$N_{\\min}$ (HARQ processes)")
    ax.set_title("Minimum HARQ Processes Required to Avoid Pipeline Stall")
    ax.legend()
    ax.grid(axis="y")
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Figure 4: GEO HARQ disable comparison
# ─────────────────────────────────────────────────────────────────────────────

def plot_geo_disable(
    snr_db: np.ndarray,
    geo_results: dict,   # output of simulate_geo_disable_comparison
) -> plt.Figure:

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    harq_kw = dict(color=COLORS["ir"],  marker="o", markevery=3, label="HARQ-IR (N=32)")
    rlc_kw  = dict(color=COLORS["rlc"], marker="s", markevery=3, label="RLC ARQ (HARQ disabled)", ls="--")

    # (a) BLER
    axes[0].semilogy(snr_db, geo_results["harq"]["bler"], **harq_kw)
    axes[0].semilogy(snr_db, geo_results["rlc"]["bler"],  **rlc_kw)
    axes[0].set_xlabel(r"$E_s/N_0$ [dB]")
    axes[0].set_ylabel("BLER")
    axes[0].set_ylim(1e-8, 1.1)
    axes[0].legend(fontsize=8)
    axes[0].grid(True)
    axes[0].set_title("(a) BLER")

    # (b) SE Goodput
    axes[1].plot(snr_db, geo_results["harq"]["se_gp"], **harq_kw)
    axes[1].plot(snr_db, geo_results["rlc"]["se_gp"],  **rlc_kw)
    axes[1].set_xlabel(r"$E_s/N_0$ [dB]")
    axes[1].set_ylabel("SE Goodput [bit/s/Hz]")
    axes[1].legend(fontsize=8)
    axes[1].grid(True)
    axes[1].set_title("(b) Spectral Efficiency")

    # (c) Latency
    axes[2].plot(snr_db, geo_results["harq"]["latency"], **harq_kw)
    axes[2].plot(snr_db, geo_results["rlc"]["latency"],  **rlc_kw)
    axes[2].set_xlabel(r"$E_s/N_0$ [dB]")
    axes[2].set_ylabel("Latency [ms]")
    axes[2].legend(fontsize=8)
    axes[2].grid(True)
    axes[2].set_title("(c) Latency")

    fig.suptitle("GEO 35.786 km: HARQ vs HARQ-Disabled (RLC ARQ)\n"
                 "[TR 38.821 Section 6.4.1 & 6.4.2]")
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Figure 5: Energy per bit
# ─────────────────────────────────────────────────────────────────────────────

def plot_energy_per_bit(
    snr_db: np.ndarray,
    energy_results: dict,  # {scheme_name: {'e_bit': array, ...}}
) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(6.5, 4.5))

    color_map = {"No HARQ": COLORS["no_harq"],
                 "CC-HARQ": COLORS["cc"],
                 "IR-HARQ": COLORS["ir"]}

    for idx, (name, res) in enumerate(energy_results.items()):
        color = color_map.get(name, list(COLORS.values())[idx])
        ax.semilogy(snr_db, res["e_bit"],
                    color=color, ls=LINESTYLES[idx],
                    marker=MARKERS[idx], markevery=4,
                    label=name)

    ax.set_xlabel(r"$E_s/N_0$ [dB]")
    ax.set_ylabel("Normalised Energy per Bit [J/bit, $P_{tx}=1$ W]")
    ax.set_title("Energy Efficiency vs SNR — LEO 600 km, $K=15$ dB")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig
