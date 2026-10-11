import matplotlib.pyplot as plt
import numpy as np

import os
# All manuscript figures are written to figures/paper/ inside the repository
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "figures", "paper")
os.makedirs(OUT_DIR, exist_ok=True)

# ==========================================
# 1. FONT CONFIGURATION & FIGURE STYLE (IEEE)
# ==========================================
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'Liberation Serif'],
    'font.size': 10,
    'axes.labelsize': 10.5,
    'axes.titlesize': 11.5,
    'xtick.labelsize': 9.5,
    'ytick.labelsize': 9.5,
    'legend.fontsize': 9,
    'mathtext.fontset': 'stix',
    'pdf.fonttype': 42,
    'ps.fonttype': 42
})

iterations = np.arange(1, 11)

# ==========================================
# 2. DATA EXTRACTION & CONVERSION TO µm
# ==========================================
# Baseline Data (mm -> µm)
bx_pos = np.array([0.0479, 0.0349, 0.0465, 0.0577, 0.0387, 0.0491, 0.0493, 0.0520, 0.0512, 0.0355]) * 1000
bx_skew = np.array([0.0924, 0.0921, 0.0802, 0.0988, 0.0971, 0.1111, 0.0982, 0.0855, 0.0998, 0.0819]) * 1000
bx_back = np.array([0.0130, 0.0064, 0.0173, 0.0213, 0.0024, 0.0137, 0.0111, 0.0212, 0.0116, 0.0064]) * 1000

# Calibrated Data (mm -> µm)
cx_pos = np.array([0.0046, 0.0024, 0.0033, 0.0047, 0.0007, 0.0041, 0.0203, 0.0081, 0.0116, 0.0113]) * 1000
cx_skew = np.array([0.0070, 0.0039, 0.0056, 0.0049, 0.0110, 0.0087, 0.0048, 0.0132, 0.0015, 0.0025]) * 1000
cx_back = np.array([0.0202, 0.0056, 0.0185, 0.0029, 0.0035, 0.0050, 0.0051, 0.0004, 0.0020, 0.0045]) * 1000

# Y-Axis Data (mm -> µm)
by_pos = np.array([0.0287, 0.0572, 0.0650, 0.0550, 0.0512, 0.0677, 0.0674, 0.0571, 0.0497, 0.0511]) * 1000
by_skew = np.array([0.0994, 0.0803, 0.0902, 0.0902, 0.0838, 0.0860, 0.0909, 0.0965, 0.0925, 0.0877]) * 1000
by_back = np.array([0.0539, 0.0176, 0.0244, 0.0172, 0.0322, 0.0156, 0.0201, 0.0176, 0.0203, 0.0251]) * 1000

cy_pos = np.array([0.0086, 0.0002, 0.0080, 0.0007, 0.0041, 0.0008, 0.0027, 0.0045, 0.0062, 0.0183]) * 1000
cy_skew = np.array([0.0029, 0.0008, 0.0047, 0.0039, 0.0044, 0.0091, 0.0014, 0.0147, 0.0009, 0.0067]) * 1000
cy_back = np.array([0.0124, 0.0033, 0.0077, 0.0060, 0.0053, 0.0137, 0.0010, 0.0019, 0.0021, 0.0150]) * 1000

# Color Scheme & Bounding Box Text
c_baseline, c_calibrated = '#D95F02', '#1B9E77'
c_base_line, c_cal_line = '#B33000', '#006622'

bbox_b = dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=c_base_line, alpha=0.9, linewidth=0.6)
bbox_c = dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=c_cal_line, alpha=0.9, linewidth=0.6)

# ==========================================
# 3. X-AXIS ITERATION PLOT
# ==========================================
fig1, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6.5, 6.2), sharex=True, layout='constrained')

# Pos Error X (Start X=2.5, Y=31 & Y=19 so they safely do not overlap)
l1, = ax1.plot(iterations, bx_pos, 'o--', color=c_baseline, markersize=4.5, linewidth=1.1, label='Baseline')
l2, = ax1.plot(iterations, cx_pos, 's-', color=c_calibrated, markersize=4.5, linewidth=1.1, label='Calibrated')
mb, sb = np.mean(bx_pos), np.std(bx_pos, ddof=1)
mc, sc = np.mean(cx_pos), np.std(cx_pos, ddof=1)
ax1.axhline(mb, color=c_base_line, linestyle=':', linewidth=1.2, alpha=0.85)
ax1.axhline(mc, color=c_cal_line, linestyle='-.', linewidth=1.2, alpha=0.85)
ax1.text(2.5, 31, f'Base MAE: {mb:.1f} $\pm$ {sb:.1f} $\mu$m', transform=ax1.transData,
         color=c_base_line, ha='left', va='center', fontsize=12, fontweight='bold', bbox=bbox_b)
ax1.text(2.5, 19, f'Cal. MAE: {mc:.1f} $\pm$ {sc:.1f} $\mu$m', transform=ax1.transData,
         color=c_cal_line, ha='left', va='center', fontsize=12, fontweight='bold', bbox=bbox_c)
ax1.set_ylabel('Pos. Error ($dX$)\n($\mu$m)', multialignment='center')
ax1.set_ylim(-5, 80)
ax1.grid(True, linestyle=':', alpha=0.5)
ax1.legend(loc='upper left', ncol=1, framealpha=0.9, edgecolor='gray', fontsize=12)

# Skew Error X
ax2.plot(iterations, bx_skew, 'o--', color=c_baseline, markersize=4.5, linewidth=1.1)
ax2.plot(iterations, cx_skew, 's-', color=c_calibrated, markersize=4.5, linewidth=1.1)
mb, sb = np.mean(bx_skew), np.std(bx_skew, ddof=1)
mc, sc = np.mean(cx_skew), np.std(cx_skew, ddof=1)
ax2.axhline(mb, color=c_base_line, linestyle=':', linewidth=1.2, alpha=0.85)
ax2.axhline(mc, color=c_cal_line, linestyle='-.', linewidth=1.2, alpha=0.85)
ax2.text(0.55, 0.52, f'Base MAE: {mb:.1f} $\pm$ {sb:.1f} $\mu$m', transform=ax2.transAxes,
         color=c_base_line, ha='center', va='center', fontsize=12, fontweight='bold', bbox=bbox_b)
ax2.text(0.55, 0.25, f'Cal. MAE: {mc:.1f} $\pm$ {sc:.1f} $\mu$m', transform=ax2.transAxes,
         color=c_cal_line, ha='center', va='center', fontsize=12, fontweight='bold', bbox=bbox_c)
ax2.set_ylabel('Skew Error ($dY$)\n($\mu$m)', multialignment='center')
ax2.set_ylim(-8, 135)
ax2.grid(True, linestyle=':', alpha=0.5)

# Backlash Error X
ax3.plot(iterations, bx_back, 'o--', color=c_baseline, markersize=4.5, linewidth=1.1)
ax3.plot(iterations, cx_back, 's-', color=c_calibrated, markersize=4.5, linewidth=1.1)
mb, sb = np.mean(bx_back), np.std(bx_back, ddof=1)
mc, sc = np.mean(cx_back), np.std(cx_back, ddof=1)
ax3.axhline(mb, color=c_base_line, linestyle=':', linewidth=1.2, alpha=0.85)
ax3.axhline(mc, color=c_cal_line, linestyle='-.', linewidth=1.2, alpha=0.85)
ax3.text(0.60, 0.82, f'Base MAE: {mb:.1f} $\pm$ {sb:.1f} $\mu$m', transform=ax3.transAxes,
         color=c_base_line, ha='center', va='center', fontsize=12, fontweight='bold', bbox=bbox_b)
ax3.text(0.60, 0.36, f'Cal. MAE: {mc:.1f} $\pm$ {sc:.1f} $\mu$m', transform=ax3.transAxes,
         color=c_cal_line, ha='center', va='center', fontsize=12, fontweight='bold', bbox=bbox_c)
ax3.set_ylabel('Backlash Error\n($\mu$m)', multialignment='center')
ax3.set_ylim(-5, 32)
ax3.grid(True, linestyle=':', alpha=0.5)
ax3.set_xlabel('Data Iteration')
ax3.set_xticks(iterations)

ax1.set_title('X-Axis Performance Across Iterations', fontweight='bold', pad=6)
fig1.savefig(os.path.join(OUT_DIR, 'x_axis_iterations.png'), dpi=300, bbox_inches='tight')
fig1.savefig(os.path.join(OUT_DIR, 'x_axis_iterations.pdf'), bbox_inches='tight')

# ==========================================
# 4. Y-AXIS ITERATION PLOT
# ==========================================
fig2, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6.5, 6.2), sharex=True, layout='constrained')

# Pos Error Y
l1, = ax1.plot(iterations, by_pos, 'o--', color=c_baseline, markersize=4.5, linewidth=1.1, label='Baseline')
l2, = ax1.plot(iterations, cy_pos, 's-', color=c_calibrated, markersize=4.5, linewidth=1.1, label='Calibrated')
mb, sb = np.mean(by_pos), np.std(by_pos, ddof=1)
mc, sc = np.mean(cy_pos), np.std(cy_pos, ddof=1)
ax1.axhline(mb, color=c_base_line, linestyle=':', linewidth=1.2, alpha=0.85)
ax1.axhline(mc, color=c_cal_line, linestyle='-.', linewidth=1.2, alpha=0.85)
ax1.text(0.60, 0.45, f'Base MAE: {mb:.1f} $\pm$ {sb:.1f} $\mu$m', transform=ax1.transAxes,
         color=c_base_line, ha='center', va='center', fontsize=12, fontweight='bold', bbox=bbox_b)
ax1.text(0.60, 0.25, f'Cal. MAE: {mc:.1f} $\pm$ {sc:.1f} $\mu$m', transform=ax1.transAxes,
         color=c_cal_line, ha='center', va='center', fontsize=12, fontweight='bold', bbox=bbox_c)
ax1.set_ylabel('Pos. Error ($dY$)\n($\mu$m)', multialignment='center')
ax1.set_ylim(-5, 80)
ax1.grid(True, linestyle=':', alpha=0.5)
ax1.legend(loc='upper left', ncol=1, framealpha=0.9, edgecolor='gray', fontsize=8.5)

# Skew Error Y
ax2.plot(iterations, by_skew, 'o--', color=c_baseline, markersize=4.5, linewidth=1.1)
ax2.plot(iterations, cy_skew, 's-', color=c_calibrated, markersize=4.5, linewidth=1.1)
mb, sb = np.mean(by_skew), np.std(by_skew, ddof=1)
mc, sc = np.mean(cy_skew), np.std(cy_skew, ddof=1)
ax2.axhline(mb, color=c_base_line, linestyle=':', linewidth=1.2, alpha=0.85)
ax2.axhline(mc, color=c_cal_line, linestyle='-.', linewidth=1.2, alpha=0.85)
ax2.text(0.55, 0.52, f'Base MAE: {mb:.1f} $\pm$ {sb:.1f} $\mu$m', transform=ax2.transAxes,
         color=c_base_line, ha='center', va='center', fontsize=12, fontweight='bold', bbox=bbox_b)
ax2.text(0.55, 0.25, f'Cal. MAE: {mc:.1f} $\pm$ {sc:.1f} $\mu$m', transform=ax2.transAxes,
         color=c_cal_line, ha='center', va='center', fontsize=12, fontweight='bold', bbox=bbox_c)
ax2.set_ylabel('Skew Error ($dX$)\n($\mu$m)', multialignment='center')
ax2.set_ylim(-8, 125)
ax2.grid(True, linestyle=':', alpha=0.5)

# Backlash Error Y
ax3.plot(iterations, by_back, 'o--', color=c_baseline, markersize=4.5, linewidth=1.1)
ax3.plot(iterations, cy_back, 's-', color=c_calibrated, markersize=4.5, linewidth=1.1)
mb, sb = np.mean(by_back), np.std(by_back, ddof=1)
mc, sc = np.mean(cy_back), np.std(cy_back, ddof=1)
ax3.axhline(mb, color=c_base_line, linestyle=':', linewidth=1.2, alpha=0.85)
ax3.axhline(mc, color=c_cal_line, linestyle='-.', linewidth=1.2, alpha=0.85)
ax3.text(0.75, 0.70, f'Base MAE: {mb:.1f} $\pm$ {sb:.1f} $\mu$m', transform=ax3.transAxes,
         color=c_base_line, ha='center', va='center', fontsize=12, fontweight='bold', bbox=bbox_b)
ax3.text(0.75, 0.42, f'Cal. MAE: {mc:.1f} $\pm$ {sc:.1f} $\mu$m', transform=ax3.transAxes,
         color=c_cal_line, ha='center', va='center', fontsize=12, fontweight='bold', bbox=bbox_c)
ax3.set_ylabel('Backlash Error\n($\mu$m)', multialignment='center')
ax3.set_ylim(-5, 65)
ax3.grid(True, linestyle=':', alpha=0.5)
ax3.set_xlabel('Data Iteration')
ax3.set_xticks(iterations)

ax1.set_title('Y-Axis Performance Across Iterations', fontweight='bold', pad=6)
fig2.savefig(os.path.join(OUT_DIR, 'y_axis_iterations.png'), dpi=300, bbox_inches='tight')
fig2.savefig(os.path.join(OUT_DIR, 'y_axis_iterations.pdf'), bbox_inches='tight')

# ==========================================
# 5. MAE COMPARISON & IMPROVEMENT (%) BAR CHART
# ==========================================
fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 4.2), layout='constrained')
width = 0.35
x_idx = np.arange(3)

# X-Axis Subplot
cat_x = ['Pos. Err\n($dX$)', 'Skew Err\n($dY$)', 'Backlash\nErr']
m_base_x = [np.mean(bx_pos), np.mean(bx_skew), np.mean(bx_back)]
s_base_x = [np.std(bx_pos, ddof=1), np.std(bx_skew, ddof=1), np.std(bx_back, ddof=1)]
m_cal_x = [np.mean(cx_pos), np.mean(cx_skew), np.mean(cx_back)]
s_cal_x = [np.std(cx_pos, ddof=1), np.std(cx_skew, ddof=1), np.std(cx_back, ddof=1)]

ax1.bar(x_idx - width/2, m_base_x, width, yerr=s_base_x, label='Baseline', color=c_baseline, capsize=3, edgecolor='black', linewidth=0.7)
ax1.bar(x_idx + width/2, m_cal_x, width, yerr=s_cal_x, label='Calibrated', color=c_calibrated, capsize=3, edgecolor='black', linewidth=0.7)
ax1.set_ylabel('MAE ($\mu$m)')
ax1.set_title('X-Axis MAE & Improvement', fontweight='bold', pad=8, fontsize=12)
ax1.set_xticks(x_idx)
ax1.set_xticklabels(cat_x)
ax1.set_ylim(0, 145)
ax1.grid(True, linestyle=':', alpha=0.5, axis='y')
ax1.legend(loc='upper right', ncol=1, framealpha=0.9, edgecolor='gray', fontsize=8.5)

for i in range(3):
    mb, mc = m_base_x[i], m_cal_x[i]
    imp = ((mb - mc) / mb) * 100
    ax1.annotate(f'{mb:.1f}\n$\pm${s_base_x[i]:.1f}', xy=(x_idx[i] - width/2, mb + s_base_x[i] + 1.5), ha='center', va='bottom', fontsize=11)
    ax1.annotate(f'{mc:.1f}\n$\pm${s_cal_x[i]:.1f}', xy=(x_idx[i] + width/2, mc + s_cal_x[i] + 1.5), ha='center', va='bottom', fontsize=11)
    max_h = max(mb + s_base_x[i], mc + s_cal_x[i])
    ax1.annotate(f'↓ {imp:.1f}%', xy=(x_idx[i], max_h + 16), ha='center', va='bottom', fontsize=14, fontweight='bold', color='#006622')

# Y-Axis Subplot
cat_y = ['Pos. Err\n($dY$)', 'Skew Err\n($dX$)', 'Backlash\nErr']
m_base_y = [np.mean(by_pos), np.mean(by_skew), np.mean(by_back)]
s_base_y = [np.std(by_pos, ddof=1), np.std(by_skew, ddof=1), np.std(by_back, ddof=1)]
m_cal_y = [np.mean(cy_pos), np.mean(cy_skew), np.mean(cy_back)]
s_cal_y = [np.std(cy_pos, ddof=1), np.std(cy_skew, ddof=1), np.std(cy_back, ddof=1)]

ax2.bar(x_idx - width/2, m_base_y, width, yerr=s_base_y, label='Baseline', color=c_baseline, capsize=3, edgecolor='black', linewidth=0.7)
ax2.bar(x_idx + width/2, m_cal_y, width, yerr=s_cal_y, label='Calibrated', color=c_calibrated, capsize=3, edgecolor='black', linewidth=0.7)
ax2.set_ylabel('MAE ($\mu$m)')
ax2.set_title('Y-Axis MAE & Improvement', fontweight='bold', pad=8, fontsize=12)
ax2.set_xticks(x_idx)
ax2.set_xticklabels(cat_y)
ax2.set_ylim(0, 145)
ax2.grid(True, linestyle=':', alpha=0.5, axis='y')
ax2.legend(loc='upper right', ncol=1, framealpha=0.9, edgecolor='gray', fontsize=8.5)

for i in range(3):
    mb, mc = m_base_y[i], m_cal_y[i]
    imp = ((mb - mc) / mb) * 100
    ax2.annotate(f'{mb:.1f}\n$\pm${s_base_y[i]:.1f}', xy=(x_idx[i] - width/2, mb + s_base_y[i] + 1.5), ha='center', va='bottom', fontsize=11)
    ax2.annotate(f'{mc:.1f}\n$\pm${s_cal_y[i]:.1f}', xy=(x_idx[i] + width/2, mc + s_cal_y[i] + 1.5), ha='center', va='bottom', fontsize=11)
    max_h = max(mb + s_base_y[i], mc + s_cal_y[i])
    ax2.annotate(f'↓ {imp:.1f}%', xy=(x_idx[i], max_h + 16), ha='center', va='bottom', fontsize=14, fontweight='bold', color='#006622')

fig3.savefig(os.path.join(OUT_DIR, 'mae_summary.png'), dpi=300, bbox_inches='tight')
fig3.savefig(os.path.join(OUT_DIR, 'mae_summary.pdf'), bbox_inches='tight')

# Show all plots
plt.show()