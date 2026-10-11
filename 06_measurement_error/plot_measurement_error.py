"""Dial Gauge vs Virtual Encoder comparison (measurement error).

Original script: `After Lulus Paper/code/plotmeasurement.py`. The plotting logic is
unchanged; only the data source (now read from CSV) and the output file destination
(now to `figures/`) changed. The measurement values are EXACTLY THE SAME as the
original script.

Usage:
    python 06_measurement_error/plot_measurement_error.py

Input  : data/processed/measurement_error/dial_vs_ve.csv
Output : figures/1_4_position_comparison_combined.png (+ .pdf) and the MAE table on screen.
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- centralized path configuration ---
_p = os.path.abspath(os.path.dirname(__file__))
while not os.path.isfile(os.path.join(_p, "config_paths.py")):
    _parent = os.path.dirname(_p)
    if _parent == _p:
        raise FileNotFoundError("config_paths.py was not found above this folder.")
    _p = _parent
sys.path.insert(0, _p)
import config_paths as CFG  # noqa: E402

# ==========================================
# 1. FONT & PLOT STYLE CONFIGURATION (IEEE)
# ==========================================
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'Liberation Serif'],
    'font.size': 10,
    'axes.labelsize': 12,
    'axes.titlesize': 11,
    'xtick.labelsize': 9.5,
    'ytick.labelsize': 9.5,
    'legend.fontsize': 10,
    'mathtext.fontset': 'stix',
    'pdf.fonttype': 42,
    'ps.fonttype': 42
})

CSV_PATH = os.path.join(CFG.OUTPUT_DIR, "measurement_error", "dial_vs_ve.csv")
df = pd.read_csv(CSV_PATH)

# ==========================================
# 2. BUILD THE 4 PANELS FROM CSV
# ==========================================
PANEL_ORDER = [("X", "forward"), ("Y", "forward"), ("X", "backward"), ("Y", "backward")]
TITLES = {("X", "forward"):  "X Forward Frame Position",
          ("Y", "forward"):  "Y Forward Frame Position",
          ("X", "backward"): "X Backward Frame Position",
          ("Y", "backward"): "Y Backward Frame Position"}
YLIMS = {("X", "forward"):  (470, 535),
         ("Y", "forward"):  (450, 520),
         ("X", "backward"): (-8, 42),
         ("Y", "backward"): (-8, 45)}

plots_data = []
for axis, frame in PANEL_ORDER:
    g = df[(df["axis"] == axis) & (df["frame"] == frame)].sort_values("iteration")
    plots_data.append({
        'title': TITLES[(axis, frame)],
        'ylabel': 'Position ($\\mu$m)',
        'dial': g["dial_um"].to_numpy(),
        'dial_err': float(g["dial_err_um"].iloc[0]),
        've': g["ve_um"].to_numpy(),
        'ylim': YLIMS[(axis, frame)],
        'legend_loc': 'upper left',
        'axis': axis,
    })

color_dial = '#D95F02'  # Dial Gauge (Orange-Red)
color_ve = '#1E9E77'    # Virtual Encoder (Teal-Green)
color_ve = '#1B9E77'
color_mean = '#7570B3'  # Purple (Mean Line)

# ==========================================
# 3. SINGLE FIGURE GENERATION (2x2 SUBPLOTS)
# ==========================================
fig, axes = plt.subplots(2, 2, figsize=(8.5, 7.0), layout='constrained')
axes_flat = axes.flatten()

combined_abs_diffs = {'X': [], 'Y': []}
print(f"Input: {CSV_PATH}\n")
print(f"{'panel':22s} {'MAE (µm)':>9s} {'std (µm)':>9s} {'n':>3s}")
print("-" * 46)

for i, p in enumerate(plots_data):
    ax = axes_flat[i]

    mean_ve = np.mean(p['ve'])
    abs_diff = np.abs(p['ve'] - p['dial'])
    mae = np.mean(abs_diff)
    std_diff = np.std(abs_diff, ddof=1)

    combined_abs_diffs[p['axis']].extend(abs_diff)
    print(f"{p['title']:22s} {mae:9.2f} {std_diff:9.2f} {len(abs_diff):3d}")

    # Virtual Encoder Plot
    ax.plot(p.get('iterations', np.arange(1, len(p['ve']) + 1)), p['ve'], 's-',
            color=color_ve, markersize=5.5, linewidth=1.3,
            label='Virtual Encoder', zorder=3)

    # Mean Line
    label_stat = f"Mean Diff: {mae:.1f} $\\pm$ {std_diff:.1f} $\\mu$m"
    ax.axhline(mean_ve, color=color_mean, linestyle='--', linewidth=1.3,
               label=label_stat, zorder=4)

    # Dial Gauge Errorbar Plot
    ax.errorbar(np.arange(1, len(p['dial']) + 1), p['dial'], yerr=p['dial_err'],
                fmt='o-', color=color_dial, ecolor=color_dial, elinewidth=1.2,
                capsize=3.5, capthick=1.2, markersize=5.5, linewidth=1.3,
                label='Dial Gauge ($\\pm 10\\,\\mu$m)', zorder=2)

    ax.set_xlabel('Iteration')
    ax.set_ylabel(p['ylabel'])
    ax.set_title(p['title'], fontweight='bold', pad=6)
    ax.set_ylim(p['ylim'])
    ax.set_xticks(np.arange(1, len(p['ve']) + 1))
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend(loc=p['legend_loc'], framealpha=0.9, edgecolor='gray')

print("-" * 46)
for axis in ('X', 'Y'):
    d = np.array(combined_abs_diffs[axis])
    print(f"{'Combined ' + axis:22s} {d.mean():9.2f} {d.std(ddof=1):9.2f} {len(d):3d}")
print()

fig.suptitle('Dial Gauge vs. Virtual Encoder Position Comparison',
             fontweight='bold', fontsize=16)

os.makedirs(CFG.FIG_DIR, exist_ok=True)
png = os.path.join(CFG.FIG_DIR, '1_4_position_comparison_combined.png')
pdf = os.path.join(CFG.FIG_DIR, '1_4_position_comparison_combined.pdf')
fig.savefig(png, dpi=300, bbox_inches='tight')
fig.savefig(pdf, bbox_inches='tight')
print(f"Figure saved: {png}")
print(f"                 {pdf}")
plt.show()
