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
# 2. DATA EXTRACTION FROM TABLES
# ==========================================
# Baseline Data
b_rmse_x = np.array([75.8, 79.1, 77.3, 79.0, 85.4, 77.1, 77.9, 72.8, 63.9, 80.8])
b_rmse_y = np.array([63.0, 69.3, 68.0, 64.4, 72.7, 63.9, 67.0, 61.7, 54.9, 68.1])
b_rmse_tot = np.array([98.6, 105.2, 103.0, 102.0, 112.1, 100.1, 102.7, 95.4, 84.3, 105.7])
b_reproj = np.array([0.1206, 0.1196, 0.1211, 0.1201, 0.1214, 0.1204, 0.1209, 0.1207, 0.1214, 0.1218])

# Calibrated Data
c_rmse_x = np.array([35.64, 34.12, 36.48, 35.16, 35.60, 34.90, 35.60, 32.92, 31.03, 32.74])
c_rmse_y = np.array([30.40, 30.11, 30.56, 30.99, 29.99, 34.43, 31.07, 30.38, 29.90, 29.69])
c_rmse_tot = np.array([46.85, 45.51, 47.59, 46.86, 46.55, 49.03, 47.25, 44.79, 43.09, 44.20])
c_reproj = np.array([0.1187, 0.1167, 0.1184, 0.1197, 0.1167, 0.1172, 0.1194, 0.1219, 0.1221, 0.1214])

# Color Scheme & Bounding Box Text
c_baseline, c_calibrated = '#D95F02', '#1B9E77'
c_base_line, c_cal_line = '#B33000', '#006622'

bbox_b = dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=c_base_line, alpha=0.9, linewidth=0.6)
bbox_c = dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=c_cal_line, alpha=0.9, linewidth=0.6)

# ==========================================
# 3. RMSE ITERATION PLOTS (LINE PLOT)
# ==========================================
fig1, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7.0, 6.8), sharex=True, layout='constrained')

# Subplot 1: RMSE X
l1, = ax1.plot(iterations, b_rmse_x, 'o--', color=c_baseline, markersize=4.5, linewidth=1.1, label='Baseline')
l2, = ax1.plot(iterations, c_rmse_x, 's-', color=c_calibrated, markersize=4.5, linewidth=1.1, label='Calibrated')
mb, sb = np.mean(b_rmse_x), np.std(b_rmse_x, ddof=1)
mc, sc = np.mean(c_rmse_x), np.std(c_rmse_x, ddof=1)
ax1.axhline(mb, color=c_base_line, linestyle=':', linewidth=1.2, alpha=0.85)
ax1.axhline(mc, color=c_cal_line, linestyle='-.', linewidth=1.2, alpha=0.85)

# RMSE text at 14pt (Base RMSE lowered slightly to y_rel=0.58)
ax1.text(0.55, 0.58, f'Base RMSE: {mb:.1f} $\pm$ {sb:.1f} $\mu$m', transform=ax1.transAxes, color=c_base_line, ha='center', va='center', fontsize=14, fontweight='bold', bbox=bbox_b)
ax1.text(0.55, 0.35, f'Cal. RMSE: {mc:.2f} $\pm$ {sc:.2f} $\mu$m', transform=ax1.transAxes, color=c_cal_line, ha='center', va='center', fontsize=14, fontweight='bold', bbox=bbox_c)
ax1.set_ylabel('RMSE X\n($\mu$m)', multialignment='center')
ax1.set_ylim(15, 105)
ax1.grid(True, linestyle=':', alpha=0.5)
ax1.legend(loc='upper left', ncol=1, framealpha=0.9, edgecolor='gray', fontsize=8.5)

# Subplot 2: RMSE Y
ax2.plot(iterations, b_rmse_y, 'o--', color=c_baseline, markersize=4.5, linewidth=1.1)
ax2.plot(iterations, c_rmse_y, 's-', color=c_calibrated, markersize=4.5, linewidth=1.1)
mb, sb = np.mean(b_rmse_y), np.std(b_rmse_y, ddof=1)
mc, sc = np.mean(c_rmse_y), np.std(c_rmse_y, ddof=1)
ax2.axhline(mb, color=c_base_line, linestyle=':', linewidth=1.2, alpha=0.85)
ax2.axhline(mc, color=c_cal_line, linestyle='-.', linewidth=1.2, alpha=0.85)

# RMSE text at 14pt (Base RMSE lowered slightly to y_rel=0.58)
ax2.text(0.55, 0.58, f'Base RMSE: {mb:.1f} $\pm$ {sb:.1f} $\mu$m', transform=ax2.transAxes, color=c_base_line, ha='center', va='center', fontsize=14, fontweight='bold', bbox=bbox_b)
ax2.text(0.55, 0.35, f'Cal. RMSE: {mc:.2f} $\pm$ {sc:.2f} $\mu$m', transform=ax2.transAxes, color=c_cal_line, ha='center', va='center', fontsize=14, fontweight='bold', bbox=bbox_c)
ax2.set_ylabel('RMSE Y\n($\mu$m)', multialignment='center')
ax2.set_ylim(10, 90)
ax2.grid(True, linestyle=':', alpha=0.5)

# Subplot 3: RMSE Total
ax3.plot(iterations, b_rmse_tot, 'o--', color=c_baseline, markersize=4.5, linewidth=1.1)
ax3.plot(iterations, c_rmse_tot, 's-', color=c_calibrated, markersize=4.5, linewidth=1.1)
mb, sb = np.mean(b_rmse_tot), np.std(b_rmse_tot, ddof=1)
mc, sc = np.mean(c_rmse_tot), np.std(c_rmse_tot, ddof=1)
ax3.axhline(mb, color=c_base_line, linestyle=':', linewidth=1.2, alpha=0.85)
ax3.axhline(mc, color=c_cal_line, linestyle='-.', linewidth=1.2, alpha=0.85)

# RMSE text at 14pt (Base RMSE lowered slightly to y_rel=0.56)
ax3.text(0.55, 0.56, f'Base RMSE: {mb:.1f} $\pm$ {sb:.1f} $\mu$m', transform=ax3.transAxes, color=c_base_line, ha='center', va='center', fontsize=14, fontweight='bold', bbox=bbox_b)
ax3.text(0.55, 0.33, f'Cal. RMSE: {mc:.2f} $\pm$ {sc:.2f} $\mu$m', transform=ax3.transAxes, color=c_cal_line, ha='center', va='center', fontsize=14, fontweight='bold', bbox=bbox_c)
ax3.set_ylabel('RMSE Total\n($\mu$m)', multialignment='center')
ax3.set_ylim(25, 130)
ax3.grid(True, linestyle=':', alpha=0.5)
ax3.set_xlabel('Data Iteration')
ax3.set_xticks(iterations)

ax1.set_title('Trajectory Test Accuracy Across Iterations', fontweight='bold', pad=6)
fig1.savefig(os.path.join(OUT_DIR, 'trajectory_rmse_iterations_final.png'), dpi=300, bbox_inches='tight')
fig1.savefig(os.path.join(OUT_DIR, 'trajectory_rmse_iterations_final.pdf'), bbox_inches='tight')

# ==========================================
# 4. COMPARISON & IMPROVEMENT (%) BAR CHART
# ==========================================
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.0, 4.6), layout='constrained', gridspec_kw={'width_ratios': [2.2, 1]})
width = 0.35
x_idx_rmse = np.arange(3)

# Left Panel: RMSE X, Y, Total
cat_rmse = ['RMSE X', 'RMSE Y', 'RMSE Total']
m_base_rmse = [np.mean(b_rmse_x), np.mean(b_rmse_y), np.mean(b_rmse_tot)]
s_base_rmse = [np.std(b_rmse_x, ddof=1), np.std(b_rmse_y, ddof=1), np.std(b_rmse_tot, ddof=1)]
m_cal_rmse = [np.mean(c_rmse_x), np.mean(c_rmse_y), np.mean(c_rmse_tot)]
s_cal_rmse = [np.std(c_rmse_x, ddof=1), np.std(c_rmse_y, ddof=1), np.std(c_rmse_tot, ddof=1)]

ax1.bar(x_idx_rmse - width/2, m_base_rmse, width, yerr=s_base_rmse, label='Baseline', color=c_baseline, capsize=3, edgecolor='black', linewidth=0.7)
ax1.bar(x_idx_rmse + width/2, m_cal_rmse, width, yerr=s_cal_rmse, label='Calibrated', color=c_calibrated, capsize=3, edgecolor='black', linewidth=0.7)

ax1.set_ylabel('RMSE ($\mu$m)')
ax1.set_title('Trajectory Accuracy Improvement', fontweight='bold', pad=8)
ax1.set_xticks(x_idx_rmse)
ax1.set_xticklabels(cat_rmse)
ax1.set_ylim(0, 185)
ax1.grid(True, linestyle=':', alpha=0.5, axis='y')
ax1.legend(loc='upper left', ncol=1, framealpha=0.9, edgecolor='gray', fontsize=9.5)

for i in range(3):
    mb, mc = m_base_rmse[i], m_cal_rmse[i]
    imp = ((mb - mc) / mb) * 100
    # Quantitative Black Text: Fontsize 12
    ax1.annotate(f'{mb:.1f}\n$\pm${s_base_rmse[i]:.1f}', xy=(x_idx_rmse[i] - width/2, mb + s_base_rmse[i] + 2), ha='center', va='bottom', fontsize=12)
    ax1.annotate(f'{mc:.2f}\n$\pm${s_cal_rmse[i]:.2f}', xy=(x_idx_rmse[i] + width/2, mc + s_cal_rmse[i] + 2), ha='center', va='bottom', fontsize=12)
    max_h = max(mb + s_base_rmse[i], mc + s_cal_rmse[i])
    # Green Percentage Text: Fontsize 14
    ax1.annotate(f'↓ {imp:.2f}%', xy=(x_idx_rmse[i], max_h + 24), ha='center', va='bottom', fontsize=14, fontweight='bold', color='#006622')

# Right Panel: Reprojection Error
x_idx_reproj = np.array([0])
m_base_rep, s_base_rep = np.mean(b_reproj), np.std(b_reproj, ddof=1)
m_cal_rep, s_cal_rep = np.mean(c_reproj), np.std(c_reproj, ddof=1)

ax2.bar(x_idx_reproj - width/2, m_base_rep, width, yerr=s_base_rep, label='Baseline', color=c_baseline, capsize=3, edgecolor='black', linewidth=0.7)
ax2.bar(x_idx_reproj + width/2, m_cal_rep, width, yerr=s_cal_rep, label='Calibrated', color=c_calibrated, capsize=3, edgecolor='black', linewidth=0.7)

ax2.set_ylabel('Reprojection Error (px)')
ax2.set_title('Reprojection Error', fontweight='bold', pad=8)
ax2.set_xticks(x_idx_reproj)
ax2.set_xticklabels(['Reprojection\nError'])
ax2.set_ylim(0, 0.175)
ax2.grid(True, linestyle=':', alpha=0.5, axis='y')
ax2.legend(loc='upper right', ncol=1, framealpha=0.9, edgecolor='gray', fontsize=9.5)

# Quantitative Black Text: Fontsize 12
ax2.annotate(f'{m_base_rep:.4f}\n$\pm${s_base_rep:.4f}', xy=(x_idx_reproj[0] - width/2, m_base_rep + s_base_rep + 0.003), ha='center', va='bottom', fontsize=12)
ax2.annotate(f'{m_cal_rep:.4f}\n$\pm${s_cal_rep:.4f}', xy=(x_idx_reproj[0] + width/2, m_cal_rep + s_cal_rep + 0.003), ha='center', va='bottom', fontsize=12)

fig2.savefig(os.path.join(OUT_DIR, 'trajectory_summary_bars_final.png'), dpi=300, bbox_inches='tight')
fig2.savefig(os.path.join(OUT_DIR, 'trajectory_summary_bars_final.pdf'), bbox_inches='tight')

plt.show()