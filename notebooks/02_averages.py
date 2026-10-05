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
# # Averages: where they settle, and in what shape
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/02_averages.ipynb)
#
# **Takeaway: averages of many independent draws from one fixed distribution pile up in a bell around the true value, and four times more draws make the bell half as wide.**
#
# This is the second notebook of the series.
# Notebook 1 showed a histogram settling onto the probabilities as the rolls piled up;
# this one shows why, and how fast.
# The next notebook looks more closely at the bell you will meet here.
# The core path takes about 15 minutes.
# Exercises marked *Stretch (optional)* can be skipped.
#
# Python practice: repeating an experiment many times in one call, one row per run.
#
# **Start here:** save your own copy with *File > Save a copy in Drive*, so your edits are kept.
# Then run the cells in order with Shift+Enter (run and move to the next cell).
# Ctrl+Enter (Cmd+Enter on a Mac) reruns a cell without moving on.

# %%
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(20261005)  # one generator for the whole notebook, as in notebook 1

# %% [markdown]
# ## A proportion is an average
#
# Toss a coin ten times, writing heads as 1 and tails as 0:

# %%
tosses = rng.integers(0, 2, size=10)
print(tosses)

# %% [markdown]
# The average of these 0s and 1s is the number of 1s divided by 10,
# which is exactly the proportion of heads.
# `.mean()` computes it:

# %%
print(tosses.mean())

# %% [markdown]
# Every bar in notebook 1 was a proportion, so every bar was an average too.
# This notebook looks at averages directly.

# %% [markdown]
# ## One row per run
#
# We will repeat short runs of tosses many times.
# A `size` with two numbers makes a table:
# here 5 runs (the rows) of 4 tosses each (the columns).

# %%
table = rng.integers(0, 2, size=(5, 4))
print(table)

# %% [markdown]
# `.mean()` averages the whole table into one number.
# `.mean(axis=1)` averages along each row instead, giving one average per run:

# %%
print(table.mean())
print(table.mean(axis=1))

# %% [markdown]
# Two numbers control every experiment below, and they mean different things:
# `N`, the number of tosses in one run (columns),
# and `runs`, how many times we repeat the run (rows).
# `runs` stays at 10000 throughout; only `N` changes.

# %%
runs = 10000

# %% [markdown]
# ## Lopsided runs: predict, then count
#
# Call a run **lopsided** if at least 3 in 4 of its tosses are heads,
# that is, if its average is 0.75 or more.
#
# **Predict first:** which is more likely to be lopsided,
# a run of 4 tosses or a run of 16 tosses?
# Choose your answer in the menu on the right side of the next cell, then run that cell.

# %%
# Choose your prediction in the menu on the right of this cell, then run the cell.
# The menu rewrites the line below; do not edit it by hand.
prediction = "choose"  # @param ["choose", "a run of 4 tosses", "a run of 16 tosses", "about the same"]

# %% [markdown]
# The next cell draws 10000 runs of 4 tosses
# and counts the lopsided ones with notebook 1's compare-then-average move:

# %%
assert prediction != "choose", "Choose your prediction in the menu on the right of the cell above, then run that cell."

means_4 = rng.integers(0, 2, size=(runs, 4)).mean(axis=1)
print((means_4 >= 0.75).mean())

# %% [markdown]
# **Your turn:** replace the `...` with the call for runs of 16 tosses,
# using the line above as your model, then run the cell.

# %%
means_16 = ...  # 10000 runs of 16 tosses, one average per run
print((means_16 >= 0.75).mean())

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# ```python
# means_16 = rng.integers(0, 2, size=(runs, 16)).mean(axis=1)
# ```
#
# Exactly 5 in 16 runs of 4 tosses are lopsided in the long run (three or four heads), about 31%,
# and your count should be close to that;
# only about 4% of 16-toss runs are.
# The same proportion, 3 in 4, is far harder to reach with more tosses,
# because a longer run's average stays closer to 0.5.
#
# </details>

# %% [markdown]
# ## The shape of the averages
#
# Each run gives one average.
# What do 10000 of them look like together?
#
# **Predict first:** sketch on paper how the averages of 64 tosses will be spread between 0 and 1.
#
# The next cell draws three histograms, one under the other on the same scale,
# for runs of 4, 16, and 64 tosses.
# The bin edges are notebook 1's half-integer edges divided by `N`,
# so each possible average sits in the middle of its own bar.
# Each panel has its own vertical scale: compare the widths, not the heights.

# %%
plt.figure(figsize=(5, 6))
row = 1
for N in [4, 16, 64]:
    means = rng.integers(0, 2, size=(runs, N)).mean(axis=1)
    plt.subplot(3, 1, row)  # 3 rows, 1 column, this is plot number `row`
    plt.hist(means, bins=np.arange(-0.5, N + 1) / N, edgecolor="white")
    plt.xlim(-0.15, 1.15)
    plt.ylabel(f"N = {N}")
    row = row + 1
plt.xlabel("average of N tosses (proportion of heads)")
plt.show()

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# Two things happen as `N` grows.
# The averages crowd closer to 0.5,
# so a long run's average is a better guess of the true proportion.
# And they take a bell shape, symmetric and highest in the middle,
# although a single toss has only two possible values, 0 and 1.
#
# </details>

# %% [markdown]
# ## How fast the bell narrows
#
# **Predict:** each time `N` is multiplied by 4, what happens to the width of the bell?
# Does it shrink 4 times, 2 times, or not at all?
#
# `means.std()` measures the spread of the averages:
# their standard deviation, the typical distance of an average from the center.

# %%
for N in [4, 16, 64]:
    means = rng.integers(0, 2, size=(runs, N)).mean(axis=1)
    print(N, means.std())

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# It halves each time: about 0.25, 0.125, 0.0625.
# Four times more tosses make the averages half as spread out;
# halving it again takes four times more still.
# Notebook 1 promised that ten times more rolls give about three times less raggedness:
# the same law, since the square root of 10 is about 3.16.
#
# </details>

# %% [markdown]
# ## Name it: the law of large numbers and the central limit theorem
#
# **In your own words:** what happened to the averages as `N` grew?
# Say it to an imaginary classmate before opening the answer.
#
# <details>
# <summary>Answer</summary>
#
# Longer runs give averages that land closer to 0.5, packed in a narrower bell,
# and the bell's width halves every time the run gets four times longer.
#
# </details>
#
# Each of these observations has a name.
#
# - The **law of large numbers**:
#   the average of many independent draws settles at the true value, here 0.5.
# - The **central limit theorem**:
#   when independent draws come from one fixed distribution with finite variance,
#   the distribution of their average becomes approximately *normally distributed*
#   as $N$ grows.
# - The **square-root law**: the spread of the average is
#
#   $$\frac{\sigma}{\sqrt{N}},$$
#
#   where $\sigma$ is the spread of a single draw.
#   For one coin toss $\sigma = 0.5$: every toss is 0 or 1, exactly 0.5 away from the mean.
#
# **For deeper mathematics:** this notebook shows the theorem's behavior, not its proof.
# Wasserman, *All of Statistics*, Sections 5.3-5.4 distinguishes the law of large
# numbers from the central limit theorem, and Appendix 5.7.2 gives a proof.
#
# The next cell computes $\sigma / \sqrt{N}$; compare it with the spreads you measured above.

# %%
sigma = 0.5  # spread of a single toss
for N in [4, 16, 64]:
    print(N, sigma / np.sqrt(N))

# %% [markdown]
# <details>
# <summary>Why the square root? (optional)</summary>
#
# For independent draws, variances add.
# A single toss has variance $\sigma^2$,
# so the sum of $N$ tosses has variance $N\sigma^2$
# and spread $\sqrt{N}\,\sigma$:
# the sum spreads out, but only like $\sqrt{N}$.
# The average is the sum divided by $N$,
# so its spread is $\sqrt{N}\,\sigma / N = \sigma/\sqrt{N}$.
# If the draws moved together instead of independently,
# their variances would not simply add, and averaging would help less.
#
# </details>
#
# Two spreads, two names you have seen on error bars:
#
# - $\sigma$, the spread of single measurements, is the **standard deviation (SD)**.
#   It describes how much individual measurements differ, and more data does not shrink it.
# - $\sigma/\sqrt{N}$, the spread of their average, is the **standard error (SE)**.
#   It describes how precisely the average pins down the true value, and it shrinks with $N$.
#
# The bell matters as much as the width.
# Because averages are approximately normal,
# error bars and the hypothesis tests later in this course
# can say how far an average is likely to land from the truth.

# %% [markdown]
# ## Averaging EEG trials
#
# In an EEG oddball experiment, the P3 is a positive wave about 300 to 500 ms after a rare stimulus.
# On a single trial it is buried in background EEG, so labs average many trials.
# **For teaching purposes, the simulation below assumes a true P3 amplitude of 6 $\mu$V
# and single-trial noise with an SD of 5 $\mu$V**,
# roughly the values in real oddball data
# (Luck et al. 2021, Psychophysiology; Kappenman et al. 2021, NeuroImage).
#
# `rng.normal(6, 5, size=...)` draws from a bell centered at 6 with SD 5.
# Its output for five trials:

# %%
print(rng.normal(6, 5, size=5))

# %% [markdown]
# **Predict, then edit:** how many trials bring the SE of the average down to 0.5 $\mu$V?
# Try 20, then 80, then your own answer, rerunning the cell each time.

# %%
n_trials = 20
trials = rng.normal(6, 5, size=(runs, n_trials))  # one row per simulated recording session
print("SD of single trials:", trials.std())
print("SE of the average:  ", trials.mean(axis=1).std())

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# About 100 trials, since $5/\sqrt{100} = 0.5$.
# With 20 trials the SE is about 1.1 $\mu$V; with 80, about 0.56: four times the trials, half the SE.
# The SD of single trials stays near 5 $\mu$V however many trials you record;
# only the SE of the average shrinks.
#
# </details>
#
# Two cautions carry over to real recordings.
# The square-root law assumes independent trials,
# but real EEG noise drifts over a session with fatigue and learning,
# so in practice the gain is somewhat smaller (Luck et al. 2021).
# And more trials sharpen each participant's average
# but never shrink the differences between participants:
# for a claim about people, `N` counts people, not trials (Boudewyn et al. 2018, Psychophysiology).
#
# ## Why average?
#
# Averaging $N$ independent measurements shrinks their noise by $\sqrt{N}$:
# four times the measurements for half the noise.
# When independent measurements come from one fixed distribution with finite variance,
# their averages pile up in a bell around the true value as $N$ grows.

# %% [markdown]
# ## Stretch (optional)
#
# > **Stretch (optional): diluted, not corrected.**
# > After a streak of heads, are tails "due" to even things out?
# > In a new cell, draw 5 sequences of 100000 tosses with `rng.integers(0, 2, size=(5, 100000))`,
# > and for the first 10, 1000, and 100000 tosses of each, print
# > the excess heads (number of heads minus half the tosses) and the proportion of heads.
#
# <details>
# <summary>Answer</summary>
#
# ```python
# sequences = rng.integers(0, 2, size=(5, 100000))
# for n in [10, 1000, 100000]:
#     heads = sequences[:, :n].sum(axis=1)
#     print(n, heads - n / 2, heads / n)
# ```
#
# The proportions settle toward 0.5, but the excess heads does not shrink:
# it typically grows, to about 1, 13, and 127 heads.
# A single sequence can wander back near zero, yet nothing pulls it back.
# The coin has no memory, so early luck is not corrected;
# it is diluted by the many tosses that follow.
#
# </details>
#
# > **Stretch (optional): more mice, not more calipers.**
# > Tumor volumes differ a lot between mice:
# > in one study, about 1270 mm$^3$ on average with an SD of about 740 mm$^3$
# > (Sipe et al. 2022, eLife; open data).
# > Measuring one tumor again with calipers varies by about 14%
# > (Jensen et al. 2008, BMC Medical Imaging), about 180 mm$^3$ here.
# > The SE of a group mean of 5 mice is about $740/\sqrt{5} \approx 330$ mm$^3$.
# > Which lowers it more: measuring each of the 5 mice three times, or using 10 mice?
# > Simulate both: give each mouse a true volume (SD about 720 between mice)
# > and add caliper error (SD 180) to each reading.
#
# <details>
# <summary>Answer</summary>
#
# ```python
# # 5 mice, each tumor measured 3 times
# true_5 = rng.normal(1270, 720, size=(runs, 5))
# reading_1 = true_5 + rng.normal(0, 180, size=(runs, 5))
# reading_2 = true_5 + rng.normal(0, 180, size=(runs, 5))
# reading_3 = true_5 + rng.normal(0, 180, size=(runs, 5))
# per_mouse = (reading_1 + reading_2 + reading_3) / 3
# print("5 mice, 3 readings each:", per_mouse.mean(axis=1).std())
#
# # 10 mice, each tumor measured once
# true_10 = rng.normal(1270, 720, size=(runs, 10))
# reading = true_10 + rng.normal(0, 180, size=(runs, 10))
# print("10 mice, 1 reading each:", reading.mean(axis=1).std())
# ```
#
# Three readings per mouse lower the SE only from about 331 to 325 mm$^3$, about 2%;
# 10 mice lower it to about 234 mm$^3$, 29% less.
# Repeated readings average out only the caliper error;
# the differences between mice, which dominate, shrink only with more mice.
# Technical replicates are not independent samples of the biology
# (Vaux, Fidler and Cumming 2012, EMBO Reports).
#
# </details>
