# 07 — Paper figures

Scripts that draw the figures of the manuscript. They are faithful copies of the author's
original plotting code in `After Lulus Paper/code/`: **data arrays, labels, colours and layout
are unchanged**. Only the comments were translated to English and each `savefig` was redirected
into `figures/paper/`, so the scripts can be run from anywhere without scattering PNGs around.

Every figure below has been regenerated from these scripts and compared against the original
files: the PNGs were **pixel-for-pixel identical** when the scripts were first copied over.

> **One deliberate exception.** `plot_environmental_noise.py` was revised afterwards: its legend
> now reports the standard deviation of the repeated readout (2.63 / 3.44 um) instead of the
> standard deviation of the absolute deviations (1.49 / 3.40 um), because the SD of folded values
> is not the dispersion of the measured quantity and it disagreed with both the manuscript text
> and the uncertainty budget. Data, layout, colours and fonts are unchanged. `figures/paper/`
> now holds the corrected render.

| Script | Figure(s) written to `figures/paper/` |
|---|---|
| `plot_axis_iterations.py` | `x_axis_iterations`, `y_axis_iterations`, `mae_summary` (`.png` + `.pdf`) |
| `plot_trajectory_rmse.py` | `trajectory_rmse_iterations_final`, `trajectory_summary_bars_final` (`.png` + `.pdf`) |
| `plot_environmental_noise.py` | `environmental_noise_with_std` (`.png` + `.pdf`) |
| `verify_environmental_noise.py` | nothing — it only checks the noise figure against the raw stills |

The fourth manuscript figure, `1_4_position_comparison_combined`, is produced by
[`../06_measurement_error/plot_measurement_error.py`](../06_measurement_error/plot_measurement_error.py),
because that script computes the measurement-error result as well as drawing it.

## Running them

```bash
python plot_axis_iterations.py
python plot_trajectory_rmse.py
python plot_environmental_noise.py
```

They only need `matplotlib` and `numpy` and they must be run with the repo's environment
(see `requirements.txt`). Output always lands in `figures/paper/`, created if missing.

## Where the numbers come from

| Figure | Source of the plotted values |
|---|---|
| `x_axis_iterations`, `y_axis_iterations`, `mae_summary` | the per-sample travel error, skew error and backlash of the 10 valid samples of the linear test, baseline and calibrated (thesis tables) |
| `trajectory_rmse_iterations_final`, `trajectory_summary_bars_final` | the per-trial RMSE of the 10 trajectory tests, baseline and calibrated (thesis tables) |
| `environmental_noise_with_std` | the position drift of a static capture sequence (machine not commanded to move) |
| `1_4_position_comparison_combined` | `data/processed/measurement_error/dial_vs_ve.csv` |

All the arrays that are hard-coded in these scripts were checked against the thesis tables and
match exactly. See `docs/03_results_and_data_locations.md`, section 6, for the verification and
for one known inconsistency between the noise figure and the noise table.

## Auditing the environmental-noise figure

`plot_environmental_noise.py` plots a hard-coded array, so on its own it cannot be checked.
`verify_environmental_noise.py` closes that gap: it re-derives the same 10 deltas from the raw
stills in `data/raw/noise_static_capture/` using the project's own detection pipeline
(EDLines → corner refinement → sorting → `solvePnP`), and prints

* the reconstructed deltas next to the published ones (they match to 0.00 µm), and
* the two statistics definitions side by side, which is where the figure and the thesis table
  part company on axis X.

```bash
python verify_environmental_noise.py                          # uses data/raw/noise_static_capture
python verify_environmental_noise.py D:/path/to/calib_stills  # or point it anywhere
```

Raw data is not tracked by git; see `data/MANIFEST.md` for the download link.
