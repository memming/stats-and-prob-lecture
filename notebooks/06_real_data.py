# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     notebook_metadata_filter: -jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Type I and Type II errors with real mice
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/06_real_data.ipynb)
#
# **Takeaway: one mean per mouse keeps false positives near 5%; counting every measurement as a mouse makes them ten times more common.**
# Data: BDNF protein in mouse cortex, 72 mice, 15 measurements per mouse (Higuera, Gardiner & Cios 2015, PLoS ONE; UCI, CC BY 4.0).
# This is this morning's "More mice, not more calipers", with real data.
#
# **Start here:** save your own copy with *File > Save a copy in Drive*, so your edits are kept.

# %% [markdown]
# ## Load the data
# Run the next cell. It reads `bdnf_mice.csv` from the course repository (or from this folder, if you have the file).

# %%
import numpy as np
import pandas as pd

try:
    d = pd.read_csv("bdnf_mice.csv", dtype={"mouse_id": str})
except FileNotFoundError:
    d = pd.read_csv("https://raw.githubusercontent.com/memming/stats-and-prob-lecture/main/data/bdnf_mice.csv", dtype={"mouse_id": str})
ctrl = d[d.genotype == "Control"]
d.groupby(["genotype", "treatment"]).mouse_id.nunique()

# %% [markdown]
# ## Helper functions
# Run this cell once. It holds the permutation test and the fake-split simulation. You do not need to read it now.

# %%
"""Reference statistics for the course: one permutation test, used everywhere.

Two independent groups, statistic = mean(b) - mean(a), two-sided.
Exact enumeration when the number of splits is small; otherwise Monte Carlo
with the plus-one p-value. Callers pass a numpy Generator for Monte Carlo.
"""

from itertools import combinations
from math import comb

import numpy as np


def perm_test(a, b, rng=None, n_resamples=9999, exact_limit=20000):
    """Return (effect, two-sided p) for mean(b) - mean(a)."""
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    pooled = np.concatenate([a, b])
    n, k = pooled.size, b.size
    observed = b.mean() - a.mean()
    if comb(n, k) <= exact_limit:
        diffs = []
        for idx in combinations(range(n), k):
            mask = np.zeros(n, dtype=bool)
            mask[list(idx)] = True
            diffs.append(pooled[mask].mean() - pooled[~mask].mean())
        diffs = np.abs(np.array(diffs))
        return float(observed), float(np.mean(diffs >= abs(observed) - 1e-12))
    rng = rng if rng is not None else np.random.default_rng()
    shuffled = rng.permuted(np.tile(pooled, (n_resamples, 1)), axis=1)
    diffs = shuffled[:, n - k :].mean(axis=1) - shuffled[:, : n - k].mean(axis=1)
    count = int(np.sum(np.abs(diffs) >= abs(observed) - 1e-12))
    return float(observed), float((count + 1) / (n_resamples + 1))


def fake_split_rejections(
    values_by_mouse,
    n_per_group,
    rng,
    n_splits,
    alpha=0.05,
    delta=0.0,
    level="mouse",
    n_resamples=999,
):
    """Fraction of random fake splits that reach p <= alpha.

    values_by_mouse: dict mouse_id -> 1-D array of that mouse's measurements.
    delta: shift added to group B, in units of the SD of mouse means (0 = true null).
    level: "mouse" tests one mean per mouse; "measurement" tests every reading (wrong).
    """
    mice = np.array(sorted(values_by_mouse))
    sd = np.std([values_by_mouse[m].mean() for m in mice], ddof=1)
    hits = 0
    for _ in range(n_splits):
        chosen = rng.permutation(mice)[: 2 * n_per_group]
        ga, gb = chosen[:n_per_group], chosen[n_per_group:]
        if level == "mouse":
            a = [values_by_mouse[m].mean() for m in ga]
            b = [values_by_mouse[m].mean() + delta * sd for m in gb]
        else:
            a = np.concatenate([values_by_mouse[m] for m in ga])
            b = np.concatenate([values_by_mouse[m] + delta * sd for m in gb])
        hits += (
            perm_test(a, b, rng=rng, n_resamples=n_resamples, exact_limit=0)[1] <= alpha
        )
    return hits / n_splits


# %% [markdown]
# ## The real question: does memantine change BDNF?
# One mean per mouse (its 15 measurements averaged).
# **Predict first:** significant or not?

# %%
means = ctrl.groupby(["mouse_id", "treatment"]).BDNF.mean().reset_index()
saline = means.loc[means.treatment == "Saline", "BDNF"]
memantine = means.loc[means.treatment == "Memantine", "BDNF"]
perm_test(saline, memantine, rng=np.random.default_rng(0))

# %% [markdown]
# ## Type I with real noise
# Take only the saline mice and split them at random into two fake groups. Nothing differs between them, so every "significant" result is a false positive.
# **Predict first:** the false-positive rate when we test one mean per mouse, and when we test every measurement as if it were a mouse.

# %%
saline_mice = {m: g.BDNF.dropna().to_numpy() for m, g in ctrl[ctrl.treatment == "Saline"].groupby("mouse_id")}
rng = np.random.default_rng(1)
for level in ["mouse", "measurement"]:
    print(level, fake_split_rejections(saline_mice, 9, rng, 200, level=level))

# %% [markdown]
# ## Type II with a known effect
# Add a known effect (`delta`, in standard deviations of the mouse means) to one fake group.
# **Predict first:** power with 3, 5, and 9 mice per group for `delta = 1.0`. Then tweak `delta`. (How to choose a sample size in advance, power analysis, comes on Day 3.)

# %%
delta = 1.0
for n in [3, 5, 9]:
    print(n, "mice per group, power:", fake_split_rejections(saline_mice, n, rng, 200, delta=delta))

# %% [markdown]
# ## Back to the real question
# The real result was p ≈ 0.29 with about 20 mice per group. Using your power results, write two sentences: does this show that memantine has no effect on BDNF?
# Then ask the AI to attack them. Paste:
# ```
# Here is my interpretation: [paste]. Act as a critical reviewer. Find the weakest claim, give a counterexample or a case where it fails, and ask me to fix it. Do not rewrite it for me.
# ```
