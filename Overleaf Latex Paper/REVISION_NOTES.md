# Revision notes — `main_new.tex`

Review of the numerical results against the original data, and the changes applied to the
manuscript. Everything below was recomputed from the raw captures in
`Folder Rapih Code & Data Thesis/data/` using the same detection and pose-estimation pipeline as
the paper; no number was changed without a recomputation behind it.

File edited: `main_new.tex` (53,658 → 54,802 characters, 17 replacements).
Working copy of the original values is kept in the git history of the code repository.

---

## 1. What changed

| # | Location in the paper | Before | After | Why |
|---|---|---|---|---|
| 1 | Abstract | dial-gauge discrepancies 3.55 / 6.25 µm | **4.96 / 7.81 µm** | The abstract quoted the magnitude of the mean signed offset, not the mean absolute discrepancy defined by eq. `eq:encoder_reference_mae` |
| 2 | IV-C, first paragraph | "The mean absolute discrepancies were 3.55 / 6.25 µm" | **4.96 / 7.81 µm** plus one sentence reporting the direction-dependent offsets (X: 3.8 forward, 3.3 backward; Y: 8.5 forward, 4.0 backward) and the net offsets after pooling (−0.2 and +2.3 µm) | Same reason; also answers the reviewer comment that Fig. 6 "shows higher values" |
| 3 | IV-C, stationary paragraph | noise levels 2.58 and 4.9 µm, SD 2.5 and 3.3 µm | mean absolute readout deviations **2.58 / 4.97 µm**, standard deviations of the repeated readout **2.63 / 3.44 µm** | The three cited values came from three different statistics (mean of \|Δ\|, magnitude of mean Δ, population SD of Δ). Now one definition per quantity, matching Fig. 6's figure |
| 4 | IV-A, eq. `eq:distortion_coeffs` | `D = [−0.0561, 0.9595, 0.0001, 0.0004]` (4 entries, "two radial and two tangential") | `D = [−0.0561, 0.9595, 0.0001, 0.0004, −5.0330]` (5 entries, "three radial and two tangential") | The calibration actually returned five coefficients; `k3 = −5.0330` is stored as `d5` in `data/processed/camera_calibration/camera_params.csv`. The paper as written was not reproducible |
| 5 | IV-C, eq. `eq:gum_uc` | `u_c = sqrt(u_A² + u_noise² + u_reproj² + u_dial²)` | `u_c = sqrt(u_A² + u_dial²)` | `u_reproj` could not be reproduced (see §3) and `u_noise` duplicates the repeatability term |
| 6 | IV-C, prose defining the terms | definitions of `u_noise` and `u_reproj` as independent contributions | one paragraph explaining that the stationary dispersion is contained in `u_A`, and that the reprojection residual is a model-fit indicator and not an uncertainty contribution | Removes double counting and an underivable number, without hiding the measurements |
| 7 | Table `tab:uncertainty_budget` | `u_A` 1.52 / 2.66; `u_noise` 1.49 / 3.40; `u_reproj` 2.96 / 2.96; `u_dial` 5.77 / 5.77; `u_c` **6.83 / 7.61**; `U` **13.66 / 15.22** | `u_A` **2.34 / 3.57**; `u_dial` 5.77 / 5.77; `u_c` **6.23 / 6.79**; `U` **12.46 / 13.57** | Arithmetic: the Y column of the old table was internally inconsistent — its own components give `u_c` = 7.79 and `U` = 15.58, exactly as the reviewer computed |
| 8 | Table footnote | "Repeatability was evaluated using N=5 repeated measurements…" | Same, plus a sentence stating that the stationary dispersion is reported separately and the reprojection residual is a model-fit indicator | Keeps the table self-explanatory |
| 9 | Comment inside the table | `% Validation pending: … u_c = 7.79, U = 15.58` | removed | Resolved |
| 10 | III, first paragraph | camera model "introduced in Section IV" | Section II (`sec:preliminaries`) | Wrong cross-reference |
| 11 | III-A, last paragraph | camera model "introduced in Section IV" | Section II | Wrong cross-reference |
| 12 | IV-A | "the camera model described in Section IV" | Section II | Wrong cross-reference |
| 13 | Conclusion | dial-gauge discrepancies 3.55 / 6.25 µm | **4.96 / 7.81 µm** | Same reason as items 1–2 |

### Item 14 — working distance (needs your physical confirmation)

| Location | Before | After |
|---|---|---|
| IV-A, setup paragraph | "at a nominal height of 260 mm above the print bed" | "with a working distance of approximately 0.60 m between the lens and the marker during acquisition", preceded by a `% REVISION NOTE` comment |

Why: the captured images are not consistent with a 260 mm working distance.

* The 49-corner grid (120 mm across, not 140 — the object points are `mgrid[0:7]×20 mm`) occupies
  **37 % of the frame width** (472 px of 1280). At 260 mm the field of view would be
  1280 × 260 / 2314.64 = **144 mm**, so the grid would have to fill **83 %** of the frame.
* The calibrated pose puts the marker centre at **595.4–597.1 mm** in three independent datasets
  (camera-calibration set, linear baseline set, stationary noise set); the marker plane is nearly
  fronto-parallel (4.6°), so this is a well-defined distance, not a tilt artefact.
* This cannot be a scale error: the dial gauge confirms the metric scale to 0.8 %
  (commanded 0.5 mm → dial 505 µm; virtual encoder 501 µm). For the distance to be 260 mm the
  marker pitch would have to be 8.74 mm instead of 20 mm, which the dial-gauge comparison rules out.

**Please confirm** with a tape measure from the lens front to the marker surface at the
acquisition pose. If the machine is no longer assembled, the value above can stay, since it is
derived from the calibrated geometry and the metric scale is validated by the dial gauge.

---

## 2. Numbers now used, and where they come from

| Quantity | Value (X / Y) | Derivation |
|---|---|---|
| Mean absolute discrepancy vs dial gauge | **4.96 / 7.81 µm** | mean of \|d_enc − d_dial\| over the ten cycles in `data/processed/measurement_error/dial_vs_ve.csv` (per condition: 4.62, 5.30 for X and 8.54, 7.08 for Y) |
| Direction-dependent mean offset | **3.82 / 3.34** (X), **8.54 / 4.00** (Y) | \|mean(VE) − dial\| per travel direction |
| Net offset over both directions | **−0.24 / +2.27 µm** | mean of the ten signed deviations |
| Stationary readout: mean absolute deviation | **2.58 / 4.97 µm** | mean of \|Δ\| over the ten static captures |
| Stationary readout: standard deviation | **2.63 / 3.44 µm** | SD of the ten Δ values (ddof = 1); 2.49 / 3.26 with ddof = 0 |
| `u_A` | **2.34 / 3.57 µm** | sample SD within a travel direction, pooled over forward and reversal, divided by √5 |
| `u_dial` | **5.77 µm** | a = 10 µm error interval, rectangular distribution, a/√3 |
| `u_c` | **6.23 / 6.79 µm** | sqrt(u_A² + u_dial²) |
| `U` (k = 2) | **12.46 / 13.57 µm** | 2·u_c |
| `k3` | **−5.0330** | `d5` in `data/processed/camera_calibration/camera_params.csv` |

Unchanged and re-verified (no edit needed): `K` (2314.64, 2328.29, 637.08, 222.87), reprojection
RMSE 0.1152 px ± 0.0076, baseline positioning 46.3 / 55.0 µm, backlash 12.4 / 24.4 µm, all
post-calibration means, standard deviations and percentage reductions in IV-D, the trajectory
results in IV-E (100.9 → 46.17 µm, 54.24 %), and the final parameter table
(79.72 / 80.40 / 13.3 / 31.4 / −9.2 / 9.213).

---

## 3. Why `u_reproj` was removed

* The value 2.96 µm cannot be derived from the stated reprojection residual. With the measured
  working distance the scale is 255 µm/px, so 0.1152 px corresponds to **29.4 µm**, ten times
  larger. A naive independent-corner average (0.1152 px × 255 µm/px / √49) gives 4.20 µm — still
  not 2.96.
* Conceptually, the corner reprojection residual measures how well the projection model fits the
  image; it is not an independent uncertainty contribution to the measured displacement, and it is
  already reflected in the observed dispersion of that displacement.

If you prefer to keep a calibration term, it should be derived explicitly (e.g. from the marker's
dimensional tolerance as a scale contribution) rather than converted from the pixel residual.

---

## 4. Still to do on your side

1. **Figure `images/Noise_Lingkungan.png`** — its legend currently reads
   `MAE X = 2.58 ± 1.49 µm` / `MAE Y = 4.97 ± 3.40 µm`, where the ± is the standard deviation of
   the *absolute* deviations. The prose now reports the standard deviation of the readout
   (2.63 / 3.44 µm). Re-plot the figure with `np.std(delta, ddof=1)` so the figure and the text
   agree; the data and everything else in the plot stay as they are.
2. **Figure `images/1_4_position_comparison_combined.png`** — the panels label the annotated number
   as "Mean Diff", but the printed values (4.6, 8.5, 5.3, 7.1 µm) are mean absolute deviations.
   Relabel to "MAE" so it matches the text and eq. `eq:encoder_reference_mae`.
3. **Working distance** — confirm item 14 above.
4. **`sections/*.tex`, `original_main.tex`, `Old_bibliography.tex`** — these are an older split
   version of the manuscript and still contain the old numbers (3.55 / 6.25, `u_c` 7.61 /
   `U` 15.22, `u_reproj` 2.96, and the noise values 2.5 / 3.3). They are not included by
   `main_new.tex`. Either delete them or keep them out of the compile path, so nobody edits the
   stale copy by mistake.

## 5. Verification performed

* All 17 replacements matched exactly once; the file was then screened for every stale value
  (3.55, 6.25, 7.61, 15.22, 6.83, 13.66, 1.52, 2.66, 1.49, 3.40, 2.96, 2.5, 3.3, 260 mm) —
  none remain.
* Structure intact: braces balanced (909 / 909), one `\begin{document}` / `\end{document}`,
  5 `\section`, 14 `\subsection`, unchanged from the original.
* Body recompiled with pdflatex to confirm the document still builds after the edits.

### Item 15 — bibliography (build-blocking, found while building the PDF)

`Bibliography.bib` in this folder originally had 13 entries and did **not** contain
`Dan2022` or `opencv_solvepnp`, so those two citations did not resolve. The copy inside
`Zayd_IEEE.zip` has 46 entries but is missing four entries the text cites:
`ahmadshah2024`, `machinetool2023`, `subpixel2024`, `visionbased2016`. Neither file was
complete on its own.

Action taken: the two files were merged (union of entries, 50 entries) into
`Bibliography.bib`. The original 13-entry version is kept as
`Bibliography_reduced_backup.bib`. After the merge, all 15 cited keys resolve and the build
reports no missing database entries.

### About the PDF files in this folder

* `main_new.pdf` — compiled from the revised `main_new.tex` (10 pages, bibliography included).
* `main_prerevision_build.pdf` — the build that shipped inside your zip. It still contains the
  old numbers (3.55 / 6.25 µm, `u_c` 7.61, `U` 15.22); renamed from `main.pdf` so it cannot be
  mistaken for the current build. Nothing else was changed; delete it if you no longer need it.
