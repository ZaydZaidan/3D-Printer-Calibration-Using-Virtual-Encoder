"""Environmental-noise figure for the manuscript.

Revision: the legend reports the standard deviation of the repeated readout
(2.63 / 3.44 um) instead of the standard deviation of the absolute deviations
(1.49 / 3.40 um). The SD of folded values is not the dispersion of the measured
quantity, so it disagreed with the uncertainty budget and with the text.
Data, layout, colours and fonts are unchanged.
"""
import matplotlib.pyplot as plt
import numpy as np

import os
# All manuscript figures are written to figures/paper/ inside the repository
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "figures", "paper")
os.makedirs(OUT_DIR, exist_ok=True)

# IEEE Transactions typography configuration
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'Liberation Serif'],
    'font.size': 14,          # Base font
    'axes.labelsize': 15,     # X & Y axis labels
    'axes.titlesize': 16,     # Plot title
    'xtick.labelsize': 14,    # X axis tick labels
    'ytick.labelsize': 14,    # Y axis tick labels
    'legend.fontsize': 12,    # Legend text
    'mathtext.fontset': 'stix',
    'pdf.fonttype': 42,
    'ps.fonttype': 42
})

iterations = np.arange(1, 11)

# Position delta from table data (in µm)
delta_x = np.array([-4.8, -2.1, -4.0, 1.1, 1.2, 0.6, -4.6, -3.1, -2.1, 2.2])
delta_y = np.array([-4.1, -6.7, -5.1, -3.0, -11.1, 0.1, -1.1, -8.7, -6.7, -3.1])

# Absolute Error (|ΔX| and |ΔY|)
abs_err_x = np.abs(delta_x)
abs_err_y = np.abs(delta_y)

# Compute Mean Absolute Error (MAE) and Standard Deviation (SD)
mae_x = np.mean(abs_err_x)
sd_x = np.std(delta_x, ddof=1)   # SD of the repeated readout itself

mae_y = np.mean(abs_err_y)
sd_y = np.std(delta_y, ddof=1)   # (not of its absolute value, which folds the bias)

color_x = '#1B9E77'  # Teal Green
color_y = '#D95F02'  # Orange Red

fig, ax = plt.subplots(figsize=(6.2, 4.4), layout='constrained')

# Plot Absolute Error per Iteration
ax.plot(iterations, abs_err_x, 's-', color=color_x, linewidth=1.4, markersize=6,
        label='Environmental Noise X-Axis', zorder=3)
ax.plot(iterations, abs_err_y, 'o-', color=color_y, linewidth=1.4, markersize=6,
        label='Environmental Noise Y-Axis', zorder=3)

# Mean absolute deviation (MAE) line, with the SD of the repeated readout in the label
ax.axhline(mae_x, color=color_x, linestyle='--', linewidth=1.3,
           label=f'MAE X = {mae_x:.2f} $\mu$m, SD = {sd_x:.2f} $\mu$m', zorder=2)
ax.axhline(mae_y, color=color_y, linestyle='--', linewidth=1.3,
           label=f'MAE Y = {mae_y:.2f} $\mu$m, SD = {sd_y:.2f} $\mu$m', zorder=2)

ax.set_xlabel('Iteration')
ax.set_ylabel('Absolute Error ($\mu$m)')
ax.set_title('Environmental Noise Evaluation', fontweight='bold', pad=8)
ax.set_xticks(iterations)
ax.set_ylim(-0.5, 14.5)
ax.grid(True, linestyle=':', alpha=0.5)

ax.legend(loc='upper right', framealpha=0.95, edgecolor='gray')

# Save figure to vector PDF and high-res PNG files
fig.savefig(os.path.join(OUT_DIR, 'environmental_noise_with_std.pdf'))
fig.savefig(os.path.join(OUT_DIR, 'environmental_noise_with_std.png'), dpi=300)
plt.show()
