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
# # Shuffling: what a drug that does nothing would show
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/03_shuffling.ipynb)
#
# **Takeaway: if a drug does nothing, its group labels are arbitrary, so shuffling them shows the differences chance alone produces; a real difference that few shuffles reach is evidence that the drug did something.**
#
# This is the third notebook of the series.
# On the coin worksheet you wrote the recipe of a hypothesis test,
# and the binomial table gave you the sampling distribution under the null hypothesis.
# Most experiments come with no such table; this notebook builds one by shuffling.
# Next, you implement a hypothesis test of your own.
# Exercises marked *Stretch (optional)* can be skipped.
#
# Python practice: shuffling an array and splitting it into two groups, repeated in a loop.
#
# **Start here:** save your own copy with *File > Save a copy in Drive*, so your edits are kept.
# Then run the cells in order with Shift+Enter (run and move to the next cell).
# Ctrl+Enter (Cmd+Enter on a Mac) reruns a cell without moving on.

# %%
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(20261005)  # one generator for the whole notebook, as in notebooks 1 and 2

# %% [markdown]
# ## Ten mice: the treated tumors are smaller
#
# Sipe et al. (2022, eLife) grew breast tumors in mice
# and injected each mouse with either anti-PD-L1, an immune checkpoint blocker,
# or a control antibody of the same type that binds nothing in the mouse.
# Here are the tumor volumes at the end of the experiment in lean mice,
# in mm$^3$, five mice per antibody
# (their open data, Figure 5B, rounded to whole mm$^3$).
# The five control mice come first, then the five anti-PD-L1 mice.
# A volume of 0 is a tumor smaller than 1 mm$^3$, about half a millimeter across.

# %%
volumes = np.array([543, 83, 555, 483, 557,  # control antibody
                    0, 70, 0, 257, 29])      # anti-PD-L1
print(volumes[:5])  # the first five: control
print(volumes[5:])  # the sixth onward: anti-PD-L1

# %% [markdown]
# The mean of each group, then the difference between them
# (rounded to one decimal with `round`):

# %%
print(volumes[:5].mean(), volumes[5:].mean())
observed = volumes[:5].mean() - volumes[5:].mean()
print(round(observed, 1))

# %% [markdown]
# The anti-PD-L1 tumors are 373 mm$^3$ smaller on average.
# But tumors differ from mouse to mouse even without treatment:
# one control tumor is 83 mm$^3$, another 557.
# Could the five anti-PD-L1 mice simply have been the ones with small tumors?

# %% [markdown]
# ## If the drug did nothing, the labels would be arbitrary
#
# Suppose anti-PD-L1 did nothing,
# and the five mice that got it were picked without regard to their tumors, as a coin would pick them.
# Then each tumor would have grown to the same size whichever antibody its mouse got,
# and any five of the ten mice could have carried the anti-PD-L1 label.
# If the labels do not matter, the real labeling should look like any shuffled one.
#
# `rng.permutation` returns the same values in a random order:

# %%
print(rng.permutation(volumes))

# %% [markdown]
# Shuffle the ten volumes, then deal the first five to "control" and the rest to "anti-PD-L1",
# as if the labels had landed on different mice:

# %%
shuffled = rng.permutation(volumes)
print(shuffled[:5], shuffled[5:])
print(round(shuffled[:5].mean() - shuffled[5:].mean(), 1))

# %% [markdown]
# Run that cell again a few times with Ctrl+Enter.
# Each run is one way the experiment could have come out if the drug did nothing.
# Did any shuffle reach 373?
#
# <details>
# <summary>Answer</summary>
#
# Rarely.
# Most shuffled differences land within a few hundred mm$^3$ of 0, on either side;
# a shuffle reaches 373 less than once in a hundred tries.
#
# </details>

# %% [markdown]
# ## Ten thousand shuffles show what a useless drug would produce
#
# The next cell repeats the shuffle 10000 times
# and collects the differences in a list, as notebook 1 collected counts,
# then draws their histogram with a black line at the real difference.
#
# **Predict first:** where will the 10000 shuffled differences center?
# Choose your answer in the menu on the right side of the next cell, then run that cell.

# %%
# Choose your prediction in the menu on the right of this cell, then run the cell.
# The menu rewrites the line below; do not edit it by hand.
prediction = "choose"  # @param ["choose", "around 0", "around 187 (half of 373)", "around 373"]

# %%
assert prediction != "choose", "Choose your prediction in the menu on the right of the cell above, then run that cell."

runs = 10000
diffs = []
for i in range(runs):
    shuffled = rng.permutation(volumes)
    diffs.append(shuffled[:5].mean() - shuffled[5:].mean())
diffs = np.array(diffs)  # an array, so that one comparison checks every shuffle at once

plt.figure(figsize=(5, 3))
plt.hist(diffs, bins=40, edgecolor="white")
plt.axvline(observed, color="black")  # the real difference
plt.xlabel("difference after shuffling, control minus anti-PD-L1 (mm$^3$)")
plt.ylabel("number of shuffles")
plt.show()

# %% [markdown]
# **What is one value in this histogram?**
# Answer in a sentence before opening the answer.
#
# <details>
# <summary>Answer</summary>
#
# One value is one shuffle:
# the mean of five mice chosen at random minus the mean of the other five,
# that is, one way the experiment could have come out if anti-PD-L1 did nothing.
#
# The differences center around 0.
# A shuffled "anti-PD-L1 group" is a random five of the same ten mice,
# as likely to hold the larger tumors as the smaller ones.
# The real difference, the black line, sits far out on the right,
# where few shuffles reach.
#
# The histogram is lumpy, not the bell of notebook 2.
# Four tumors are far larger than the rest (483 to 557 mm$^3$),
# and the humps come from how many of those four a shuffle deals to each group,
# and where the 257 mm$^3$ tumor goes.
# A bell needs averages of many draws; five mice per group are too few.
# The shuffles do not need a bell: we only count them.
#
# </details>

# %% [markdown]
# ## A p-value counts the shuffles that do as well
#
# On the coin worksheet, the binomial table told you how often an honest coin
# gives a result at least as extreme as the dealer's.
# Here the shuffled differences play the role of that table.
# The question before the experiment was whether anti-PD-L1 shrinks tumors,
# so we count in that one direction:
# the shuffles whose difference is at least as large as the real one.
#
# **Your turn:** replace the `...` with the fraction of shuffles
# whose difference is at least `observed`,
# using notebook 1's compare-then-average move, then run the cell.

# %%
p_value = ...  # fraction of shuffles with a difference at least as large as observed
print(p_value)

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# ```python
# p_value = (diffs >= observed).mean()
# ```
#
# About 0.008, give or take a few thousandths from one set of 10000 shuffles to the next:
# fewer than 1 shuffle in 100 does as well as the real labels.
# This fraction is the p-value from the board.
# Most papers count both directions, as you did at the board for the coin:
# `(np.abs(diffs) >= observed).mean()` gives about 0.016, twice as large.
#
# </details>
#
# <details>
# <summary>Why whole numbers? (optional)</summary>
#
# A computer adds decimals with tiny rounding errors that depend on the order:
# `0.1 + 0.2 + 0.3` gives `0.6000000000000001`, but `0.3 + 0.2 + 0.1` gives `0.6`.
# A shuffle that deals the real five mice into the control group, in a different order,
# could then land a hair below `observed`, and `>=` would miss it,
# making the p-value too small.
# Sums of whole numbers are exact in any order, so the volumes here are rounded to whole mm$^3$.
# With decimal data, compare against a hair less than the observed value:
# `(diffs >= observed - 1e-9).mean()`.
#
# </details>
#
# <details>
# <summary>Why 252? (optional)</summary>
#
# There are $\binom{10}{5} = 252$ ways to choose which five of the ten mice carry the anti-PD-L1 label,
# the worksheet's "$n$ choose $k$".
# If the drug does nothing, all 252 are equally likely,
# and the 10000 shuffles sample them at random.
# Only 2 of the 252 give a difference of 373 mm$^3$ or more:
# the real labeling, and the one that swaps the 257 mm$^3$ anti-PD-L1 tumor
# with the 83 mm$^3$ control tumor (a difference of 442.6).
# So the exact p-value is $2/252 \approx 0.008$.
# Your 10000 shuffles estimate this fraction.
#
# </details>
#
# <details>
# <summary>Why some add 1 (optional)</summary>
#
# The real labeling is itself one of the possible shuffles.
# Counting it, $p = (1 + b)/(1 + m)$, where $b$ of $m$ shuffles are at least as extreme.
# This p-value is valid for any number of shuffles:
# a test that rejects when $p \le 0.05$ rejects a true null hypothesis at most 5% of the time
# (Ernst 2004, Statistical Science, Section 4.2;
# Phipson and Smyth 2010, Statistical Applications in Genetics and Molecular Biology).
# With 10000 shuffles it differs from yours by at most 0.0001.
# The difference matters when no shuffle reaches the real difference:
# the rule then gives $p = 1/10001$, about 0.0001, the smallest p-value 10000 shuffles can show.
# Never report $p = 0$.
#
# </details>

# %% [markdown]
# ## Shuffling tests the null hypothesis of independence
#
# **In your own words:** what did the shuffles show?
# Say it to an imaginary classmate before opening the answer.
#
# <details>
# <summary>Answer</summary>
#
# If the drug did nothing, the labels would be arbitrary,
# and shuffling them gives differences centered on 0,
# almost all of them closer to 0 than 373 mm$^3$.
# Fewer than 1 shuffle in 100 does as well as the real labels,
# so the real labels do not look arbitrary: evidence that the drug did something.
#
# </details>
#
# - The **null hypothesis of independence**: tumor volume does not depend on which antibody the mouse got.
#   Under it, and if the mice that got the drug were picked without regard to their tumors,
#   the ten volumes are **exchangeable**:
#   reordering them does not change how likely they are,
#   so every one of the 252 labelings is equally likely.
#   That is why the shuffled differences, given these ten volumes,
#   are the sampling distribution under the null hypothesis,
#   step 3 of your worksheet recipe.
# - The worksheet recipe with shuffling in step 3 is the **permutation test**,
#   also called a shuffle test or randomization test.
#   Its p-value is
#
#   $$p = \frac{\text{number of shuffles with a difference at least as large as the observed one}}{\text{number of shuffles}}.$$
#
# - The null hypothesis says the label does not matter at all, which is stronger than "the means are equal".
#   If two groups differ in spread but not in mean,
#   the shuffle test of the difference in means is no longer exact:
#   it can reject equal means more often than its level promises
#   (Romano 1990, JASA; Chung and Romano 2013, Annals of Statistics).
#
# **For deeper mathematics:** Ernst (2004), "Permutation methods: a basis for exact inference",
# *Statistical Science* 19:676-685, Sections 3-4, proves by counting why the permutation test is exact,
# separates random assignment from random sampling, and derives the add-one rule.
# Lehmann and Romano, *Testing Statistical Hypotheses*, Section 15.2, gives the general theorem.

# %% [markdown]
# ## The same drug in obese mice: almost as large a difference
#
# Sipe et al. ran the same experiment in obese mice.
# Their tumor volumes, again in whole mm$^3$, control mice first:

# %%
volumes_obese = np.array([4540, 2019, 2127, 1928, 1759,  # control antibody
                          675, 2375, 1679, 3977, 2194])  # anti-PD-L1
print(volumes_obese[:5])
print(volumes_obese[5:])
observed_obese = volumes_obese[:5].mean() - volumes_obese[5:].mean()
print(round(observed_obese, 1))

# %% [markdown]
# The anti-PD-L1 tumors are 295 mm$^3$ smaller on average,
# almost as large a difference as the lean mice's 373.
#
# **Predict first:** how often will a shuffle of the obese mice reach 295?
# Choose your answer in the menu on the right side of the next cell, then run that cell.

# %%
# Choose your prediction in the menu on the right of this cell, then run the cell.
# The menu rewrites the line below; do not edit it by hand.
prediction_obese = "choose"  # @param ["choose", "rarely, as for the lean mice", "often", "never"]

# %% [markdown]
# The next cell repeats the shuffles of the lean mice on the obese mice.
# Its histogram has its own scale, about three times wider than the lean one:
# look at where the black line falls, not at the width.

# %%
assert prediction_obese != "choose", "Choose your prediction in the menu on the right of the cell above, then run that cell."

diffs_obese = []
for i in range(runs):
    shuffled = rng.permutation(volumes_obese)
    diffs_obese.append(shuffled[:5].mean() - shuffled[5:].mean())
diffs_obese = np.array(diffs_obese)

plt.figure(figsize=(5, 3))
plt.hist(diffs_obese, bins=40, edgecolor="white")
plt.axvline(observed_obese, color="black")  # the real difference
plt.xlabel("difference after shuffling, control minus anti-PD-L1 (mm$^3$)")
plt.ylabel("number of shuffles")
plt.show()

print("p-value:", (diffs_obese >= observed_obese).mean())

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# Often: about 1 shuffle in 3 reaches 295 (p about 0.34).
# The obese tumors vary far more than the lean ones;
# the control tumors alone range from 1759 to 4540 mm$^3$.
# Dealing such different tumors into two groups at random
# routinely produces differences of 295 mm$^3$ or more.
# The three humps show how:
# a shuffle that deals the two largest tumors, 4540 and 3977 mm$^3$, into the same group
# gives a difference of about 400 to 1430 mm$^3$ either way, mostly the outer humps;
# one that splits them gives less than 650, the middle hump, where 295 falls.
# The size of a difference does not say whether chance could produce it; the shuffles do.
#
# A large p-value is not evidence that the drug fails in obese mice.
# It says only that shuffles often produce a difference of 295;
# with tumors this variable, five mice per group cannot tell a modest effect from none.
#
# </details>

# %% [markdown]
# ## You can now...
#
# test whether a difference between two groups could come from chance alone, with no formula:
# shuffle the labels, recompute the difference, and count how often a shuffle does as well.
# `scipy.stats.permutation_test` does the same in one call, now that you know what it computes;
# it counts both directions unless told otherwise.
#
# Shuffle the units that can trade labels under the null hypothesis: here, the mice.
# A hundred cells from one mouse do not stand in for a hundred mice,
# and the time points of one recording cannot be shuffled as if they were independent:
# neighboring time points resemble each other, so shuffling them makes chance look smaller than it is
# and produces false positives
# (Harris 2020, bioRxiv; Elber-Dorozko and Loewenstein 2018, eLife).
# As in notebook 2, count mice, not cells or time points.
#
# ## Why shuffle?
#
# If the labels do not matter, shuffling them shows what chance alone would produce.
# The p-value is how often a shuffle does at least as well as the real labels.

# %% [markdown]
# ## Stretch (optional)
#
# > **Stretch (optional): CD8+ T cells in lean and obese tumors.**
# > Sipe et al. also measured CD8+ T cells, the cytotoxic T cells whose brake anti-PD-L1 releases,
# > in each tumor (open data, Figure 4B, as whole cells per 10000 live cells):
# > lean mice 104, 74, 31, 66, 38, 43, 22, 49;
# > obese mice 28, 38, 28, 20, 20, 16, 22.
# > In a new cell, test whether lean tumors hold more CD8+ T cells.
# > The groups have 8 and 7 mice, so the split falls after the eighth value, not the fifth.
#
# <details>
# <summary>Answer</summary>
#
# ```python
# cd8 = np.array([104, 74, 31, 66, 38, 43, 22, 49,  # lean
#                 28, 38, 28, 20, 20, 16, 22])      # obese
# observed_cd8 = cd8[:8].mean() - cd8[8:].mean()
#
# diffs_cd8 = []
# for i in range(runs):
#     shuffled = rng.permutation(cd8)
#     diffs_cd8.append(shuffled[:8].mean() - shuffled[8:].mean())
# diffs_cd8 = np.array(diffs_cd8)
# print(observed_cd8, (diffs_cd8 >= observed_cd8).mean())
# ```
#
# Lean tumors hold about 29 more CD8+ T cells per 10000 live cells, and p is about 0.003:
# exactly 20 of the 6435 ways to split the 15 mice into groups of 8 and 7 do as well.
# The loop is unchanged; only the split moved.
#
# </details>
#
# > **Stretch (optional): two neurons, shuffled trials.**
# > Two nearby neurons shown the same stimulus again and again
# > tend to fire above their average on the same trials:
# > a *noise correlation*, typically 0.1 to 0.2 (Cohen and Kohn 2011, Nature Neuroscience).
# > **For teaching purposes, these three lines simulate two such neurons on 200 trials,
# > sharing an input that varies from trial to trial:**
# >
# > ```python
# > shared = rng.poisson(1, size=200)      # input common to both neurons, one value per trial
# > a = shared + rng.poisson(5, size=200)  # spike counts of neuron A
# > b = shared + rng.poisson(5, size=200)  # spike counts of neuron B
# > ```
# >
# > `np.corrcoef(a, b)[0, 1]` is their correlation.
# > Shuffling the trials of neuron B keeps every one of its spike counts
# > but breaks the pairing of the two neurons' trials,
# > the standard way to remove noise correlations from real recordings (Kafashan et al. 2021, Nature Communications).
# > In a new cell, test whether the two neurons fire together more than chance would produce.
#
# <details>
# <summary>Answer</summary>
#
# ```python
# observed_r = np.corrcoef(a, b)[0, 1]
#
# rs = []
# for i in range(runs):
#     rs.append(np.corrcoef(a, rng.permutation(b))[0, 1])
# rs = np.array(rs)
# print(observed_r, (rs >= observed_r).mean())
# ```
#
# Each simulated count has variance $1 + 5 = 6$, of which the shared input contributes 1,
# so the true correlation is $1/6 \approx 0.17$.
# Your observed correlation is likely somewhere between 0.05 and 0.3,
# and in about 3 of 4 simulated sessions the p-value falls below 0.05.
# Rerun the three simulation lines and the test a few times:
# a real correlation this weak is not always detectable with 200 trials.
#
# </details>
