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
# # How many rolls before a histogram looks like the die?
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/01_random_sampling.ipynb)
#
# **Takeaway: a histogram of a few rolls looks far less like the die than you would expect; only many rolls reveal it.**
#
# This is the first notebook of the series; the next one is the law of large numbers.
# The core path takes about 15-20 minutes.
# Exercises marked *Stretch (optional)* can be skipped.
#
# Python practice: drawing random samples with numpy.
#
# **Start here:** save your own copy with *File > Save a copy in Drive*, so your edits are kept.
# Then run the cells in order with Shift+Enter (run and move to the next cell).
# Ctrl+Enter (Cmd+Enter on a Mac) reruns a cell without moving on.

# %%
import matplotlib.pyplot as plt
import numpy as np

# %% [markdown]
# ## A generator makes the random numbers
#
# Everything random in this notebook comes from one *random number generator*, created once, here.
# The number in parentheses is its *seed*:
# the same seed gives the same sequence,
# so when you rerun the notebook from the top every figure comes back the same.
#
# Look at what the call returns: the generator itself, not a number.
# We ask it for numbers next.

# %%
rng = np.random.default_rng(20261005)
print(rng)

# %% [markdown]
# ## One roll is unpredictable
#
# `rng.integers(1, 7)` asks for a whole number from 1 up to, **but not including**, 7:
# one roll of a die.
# Run the cell below several times with Ctrl+Enter. Do you get the same answer?

# %%
print(rng.integers(1, 7))

# %% [markdown]
# **Predict:** what number can `rng.integers(1, 6)` never return?
# Try it in the cell above, run it a few times, then change it back to 7.
#
# <details>
# <summary>Answer</summary>
#
# 6. The upper bound is excluded, so `rng.integers(1, 6)` is a five-sided die.
# This is the most common bug with `integers`: to include the top value, add one to it.
#
# </details>

# %% [markdown]
# ## Ten rolls in one call
#
# Rerunning a cell ten times to get ten rolls is tedious.
# `rng.integers` returns many rolls at once if you give it one more argument,
# `size`, the number of rolls you want.
#
# **Your turn:** edit the call below so that it returns ten rolls, then run it.
# Right now it returns one.

# %%
rolls = rng.integers(1, 7)  # edit this call: ten rolls
print(rolls)

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# `rolls = rng.integers(1, 7, size=10)`.
# The result is an *array*: ten rolls in one object, printed in square brackets.
#
# </details>

# %% [markdown]
# ## Counting the threes
#
# To count how often a face came up, first compare every roll with it.
# The output has one `True` or `False` per roll:

# %%
print(rolls == 3)

# %% [markdown]
# Python counts each `True` as 1 and each `False` as 0,
# so `.sum()` counts the threes.
# Check it by eye against your ten rolls.

# %%
print((rolls == 3).sum())

# %% [markdown]
# The same count for every face, with the `for` loop you already know:

# %%
for face in range(1, 7):
    print(face, (rolls == face).sum())

# %% [markdown]
# ## A histogram is the count table, drawn
#
# `plt.hist` does this counting for you and draws one bar per face.
# It needs the bin *edges*, the boundaries between bars.
# Halfway points put each face in the middle of its own bar:

# %%
edges = np.arange(0.5, 7)
print(edges)

# %% [markdown]
# Every roll between two edges lands in that bar.
# Compare the bar heights with your count table above.
# One thing the histogram no longer shows is the *order* of the rolls:
# it keeps only how many of each.

# %%
plt.figure(figsize=(5, 3))
plt.hist(rolls, bins=edges, edgecolor="white")
plt.locator_params(axis="y", integer=True)  # counts are whole numbers
plt.xlabel("face")
plt.ylabel("number of rolls")
plt.show()

# %% [markdown]
# ## Sixty rolls: predict before you look
#
# A fair die rolled 60 times should show each face about 10 times.
# The cell after next rolls 60 times and shades the range from 8 to 12 rolls.
# This is an arbitrary but useful teaching band: plus or minus two rolls,
# or 20%, around the expected count of 10 for each face.
# Let's call a run **balanced** if all six bars end inside this chosen band,
# that is, if every face came up between 8 and 12 times.
# A run outside the band can still come from a fair die; this is not a test of fairness.
#
# **Predict first:** if you do this 60-roll experiment 10 times,
# how many of the 10 runs will be balanced?
# Choose your answer in the menu on the right side of the next cell, then run that cell.

# %%
# Choose your prediction in the menu on the right of this cell, then run the cell.
# The menu rewrites the line below; do not edit it by hand.
prediction = "choose"  # @param ["choose", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

# %%
assert prediction != "choose", "Choose your prediction in the menu on the right of the cell above, then run that cell."

rolls_60 = rng.integers(1, 7, size=60)
plt.figure(figsize=(5, 3))
plt.axhspan(8, 12, color="0.9")  # shaded range: 8 to 12 rolls
plt.hist(rolls_60, bins=edges, edgecolor="white")
plt.locator_params(axis="y", integer=True)  # counts are whole numbers
plt.xlabel("face")
plt.ylabel("number of rolls")
plt.show()

# %% [markdown]
# Now run that cell 10 times with Ctrl+Enter, keeping a tally of the balanced runs.
#
# <details>
# <summary>Answer</summary>
#
# Only about 8% of 60-roll runs land inside our chosen 8-to-12 band for every face,
# so in 10 runs you will most likely see one balanced run or none.
# Falling outside that arbitrary band does not make the die suspicious.
# The most and least common faces typically differ by about 8 rolls.
#
# Small samples are far more ragged than intuition expects.
# Tversky and Kahneman (1971) named the belief that they should not be
# "the law of small numbers".
#
# </details>

# %% [markdown]
# ## More rolls, same die
#
# Here is one long run of 6000 rolls, drawn once.
# `many_rolls[:20]` shows its first 20:

# %%
many_rolls = rng.integers(1, 7, size=6000)
print(many_rolls[:20])

# %% [markdown]
# The next cell looks at the first `N` of these rolls,
# so changing `N` changes nothing else.
# The bars would grow with `N`,
# so they now show the *proportion* of rolls (count divided by `N`) on a fixed scale.
#
# **Predict, then edit:** change `N` from 60 to 600, then to 6000, rerunning the cell each time.
# Before each run, decide: will the bars get more or less ragged?

# %%
N = 60
sample = many_rolls[:N]
plt.figure(figsize=(5, 3))
# density=True divides each count by N here, because every bar is 1 wide
plt.hist(sample, bins=edges, density=True, edgecolor="white")
plt.ylim(0, 0.35)
plt.xlabel("face")
plt.ylabel("proportion of rolls")
plt.title(f"first {N} rolls")
plt.show()

# %% [markdown]
# The height of the first bar, computed directly from the rolls,
# and one sixth as a decimal for comparison
# (rerun this cell after changing `N`):

# %%
print((sample == 1).sum() / N)  # proportion of ones among the first N rolls
print(1 / 6)

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# Less ragged.
# The largest gap between a bar and the level the bars settle toward
# is typically about 0.07 at N = 60, 0.02 at N = 600, and under 0.01 at N = 6000.
# Each tenfold increase in N shrinks it about threefold;
# the next notebook shows why.
#
# </details>

# %% [markdown]
# ## Name it: the empirical distribution approaches the probability
#
# **In your own words:** what happened to the histogram as `N` grew?
# Say it to an imaginary classmate before opening the answer.
#
# <details>
# <summary>Answer</summary>
#
# With few rolls the bars are ragged and change from run to run.
# With many rolls they flatten out at the same height for every face,
# and the shape stops changing.
#
# </details>
#
# The bar heights are the **empirical distribution**:
# the proportion of rolls that showed each face,
#
# $$\text{proportion of face } k = \frac{n_k}{N},$$
#
# where $n_k$ is the number of rolls showing $k$.
# The cell `(sample == 1).sum() / N` above computes it for $k = 1$.
#
# The level the bars settle toward, $1/6$ (about 0.167) for every face of a fair die,
# is the **probability** of each face.
# With many rolls the empirical distribution approaches the probabilities;
# with few, it can be far from them.

# %%
plt.figure(figsize=(5, 3))
plt.hist(many_rolls, bins=edges, density=True, edgecolor="white")
plt.axhline(1 / 6, color="black", linestyle="--")  # probability of each face
plt.ylim(0, 0.35)
plt.xlabel("face")
plt.ylabel("proportion of rolls")
plt.title("all 6000 rolls; dashed line: probability 1/6")
plt.show()

# %% [markdown]
# ## A flow cytometry tube is a loaded die
#
# A gate on CD3+ T cells sorts each event into one of four categories.
# Roszczyk et al. (2024, Table 2) report group mean frequencies for 61 healthy adults.
# We divide its mean frequencies for CD4+, CD8+, DN, and DP cells by its mean CD3+
# frequency to make this simplified distribution conditional on an event being CD3+:
#
# | CD4+ | CD8+ | double negative (DN) | double positive (DP) |
# |---|---|---|---|
# | 0.589 | 0.345 | 0.056 | 0.010 |
#
# These are derived from group means, not donor-level average proportions.
#
# Each event is one roll of a loaded four-sided die.
# **For teaching purposes, we give the simulation the true proportions,
# so that any raggedness you see comes from sampling alone.
# A real tube never tells you them, and they differ from donor to donor.**
#
# `rng.choice` rolls such a die:
# give it the categories, how many events, and their probabilities `p`.
# Its output for 10 events:

# %%
cell_types = ["CD4+", "CD8+", "DN", "DP"]
p_cell = [0.589, 0.345, 0.056, 0.010]
print(rng.choice(cell_types, size=10, p=p_cell))

# %% [markdown]
# Now a whole tube of `n_events` events.
# The categories are labels, not numbers,
# so this is a bar chart of counts, not a histogram.
#
# **Predict, then edit:** with 100 events, will you see any double-positive cells?
# Try 100, then 200, then 10000, and rerun each a few times.

# %%
n_events = 100
events = rng.choice(cell_types, size=n_events, p=p_cell)
counts = []
for cell_type in cell_types:
    counts.append((events == cell_type).sum())
plt.figure(figsize=(5, 3))
plt.bar(cell_types, counts)
plt.ylabel("number of events")
plt.title(f"{n_events} events")
plt.show()

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# With 100 events the DP bar is empty about 37% of the time
# ($0.99^{100} \approx 0.37$), and with 200 events still about 13%.
# A population of 1% needs thousands of events before its bar is stable,
# which is why rare populations call for many acquired events.
#
# </details>
#
# ## You can now...
#
# draw random samples with `rng.integers` and `rng.choice`,
# count them, and draw their histogram;
# and, for any measurement that sorts things into categories,
# see how many observations its histogram needs before it resembles the truth.
#
# ## What is probability?
#
# Empirically, the probability of an outcome is the proportion its bar settles to
# as the number of draws grows.
# With independent draws from a fixed probability distribution,
# the histogram converges to its probabilities:
# $1/6$ for each face of a fair die,
# and, in our simplified flow-cytometry model, 0.589, 0.345, 0.056, 0.010
# for the four cell types.
# Why it converges, and how fast, is the subject of the next notebook.

# %% [markdown]
# ## Stretch (optional)
#
# > **Stretch (optional): a synapse is a coin.**
# > Each presynaptic spike either releases a vesicle or fails.
# > Across the terminals of one axon, release probability ranged from 0.09 to 0.54
# > (Rosenmund et al. 1993, Science).
# > In a new cell, simulate 50 spikes at a terminal with release probability 0.2,
# > count the releases, and find how many spikes you need
# > before the proportion of releases stays close to 0.2.
#
# <details>
# <summary>Answer</summary>
#
# ```python
# outcomes = rng.choice(["release", "failure"], size=50, p=[0.2, 0.8])
# print((outcomes == "release").sum() / 50)
# ```
#
# With 50 spikes the proportion typically lands anywhere from about 0.1 to 0.3;
# it takes several hundred spikes to pin it within a few hundredths.
# Real terminals are not this simple:
# a spike that closely follows another releases with a different probability.
#
# </details>
#
# > **Stretch (optional): default bins.**
# > In a new cell, run `plt.hist(many_rolls)` with no `bins`, then `plt.show()`.
# > Why are there gaps, and why do 5 and 6 sit side by side?
#
# <details>
# <summary>Answer</summary>
#
# Without `bins`, `plt.hist` makes 10 equal bins from the smallest roll (1) to the largest (6),
# each 0.5 wide.
# Four of those bins contain no whole number, which leaves the gaps,
# and the last two bins hold 5 and 6 with no empty bin between them.
# For whole-number data, always choose the edges yourself.
#
# </details>
#
# > **Stretch (optional): what random looks like.**
# > Write 100 heads and tails *by hand*, as random as you can make them,
# > then find the longest run of the same side in your sequence
# > and in 100 tosses from `rng.choice(["H", "T"], size=100)`.
#
# <details>
# <summary>Answer</summary>
#
# In 100 fair tosses the longest run is typically about 7,
# and it is 5 or longer 97% of the time.
# Sequences written by hand usually stop short of that:
# people expect randomness to alternate more than it does
# (Bar-Hillel and Wagenaar 1991; Schilling 1990).
#
# </details>
