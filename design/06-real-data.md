# Notebook 6: errors with real data - design

Status: drafted 2026-10-06 by Hyungju Jeon for the Day 2 afternoon session; not yet reviewed by Memming.
Implemented in `notebooks/06_real_data.py`, paired with `.ipynb` for Colab.
Data: `data/bdnf_mice.csv` (source and licence in `data/bdnf_mice_SOURCE.txt`).

## Where it sits

Day 2 afternoon, last part. It repeats the coin questions with real noise and a known truth,
and takes up the morning's stretch exercise "More mice, not more calipers".

## Observation and steps

Takeaway: one mean per mouse keeps false positives near 5%;
counting every measurement as a mouse makes them about ten times more common.

- BDNF protein in mouse cortex, 72 mice with 15 measurements each, memantine or saline
  (Higuera, Gardiner & Cios 2015, PLoS ONE; UCI Machine Learning Repository, CC BY 4.0).
- The real question, one mean per mouse: p ≈ 0.29.
- Type I with real noise: random fake splits of saline mice.
  False positives about 6% at the mouse level and about 49% when each measurement counts as a mouse.
- Type II with a known effect: add a 1 SD shift; power with 3, 5, and 9 mice per group (about 0.00, 0.25, 0.5).
  With 3 mice per group there are only 20 splits, so p can never reach 0.05.
- AI step: the student writes two sentences on what the result means, and the AI attacks the weakest claim.

The notebook reads the data from this repository, so it works in Colab without an upload.
