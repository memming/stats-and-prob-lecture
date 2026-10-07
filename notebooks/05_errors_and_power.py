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
# # The dealer's coin: check your answers by simulation
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/05_errors_and_power.ipynb)
#
# **Takeaway: a simulation is a quick way to check a hand calculation, and to see what changes when you change one thing.**
# Work each question on paper first, from the slides. Then run the matching cell, compare its number with yours, and try the change it suggests.
# The AI prompts are here so you can copy them.
#
# **Start here:** save your own copy with *File > Save a copy in Drive*, so your edits are kept.

# %%
import numpy as np

rng = np.random.default_rng(20261005)
runs = 100000  # games simulated per check


def flips(p, n):
    """Heads in n flips of a coin that lands heads with probability p, for each of `runs` games."""
    return (rng.random(size=(runs, n)) < p).sum(axis=1)


def accuse(heads, lo=1, hi=9):
    """Your rule: accuse on lo or fewer heads, or hi or more."""
    return (heads <= lo) | (heads >= hi)


# %% [markdown]
# ## How often does the rule accuse an honest dealer?
# Compare with your answer from the fair-coin table.
#
# **Change:** accuse also on 2 or 8 heads (`lo=2, hi=8`).

# %%
accuse(flips(0.5, 10)).mean()

# %% [markdown]
# ## Catching a cheater, and the power curve
# Compare with your P(accuse) for each coin.
#
# **Change:** use 20 flips with the rule `lo=5, hi=15`. How does the curve change?

# %%
for p in [0.5, 0.6, 0.7, 0.8, 0.9]:
    print(p, accuse(flips(p, 10)).mean().round(3))

# %% [markdown]
# **AI step.** Write your own idea first, then ask the AI tutor:
# ```
# My rule: flip 10 times, accuse on 0, 1, 9 or 10 heads. The chance of catching a cheater is 0.048 (60% coin), 0.15 (70%), 0.38 (80%), 0.74 (90%). Can its Type II error rate be one number? My idea: [your idea]. Do not give me the answer; ask me one question at a time.
# ```

# %% [markdown]
# **AI step.** Visualise the power curve:
# ```
# Make one self-contained HTML page that plots the power curve of this rule (flip 10 times, accuse on 0, 1, 9, or 10 heads): the chance of accusing against how often the coin lands heads, with a slider for the number of flips.
# ```
# Check the page against the numbers above.

# %% [markdown]
# ## The trade-off between α and β
# Compare with your hand calculation for the wider rule.
#
# **Change:** try other rules, and other numbers of flips.

# %%
for lo, hi in [(0, 10), (1, 9), (2, 8)]:
    print(f"accuse on <= {lo} or >= {hi}:", "alpha", accuse(flips(0.5, 10), lo, hi).mean().round(3),
          "power (70% coin)", accuse(flips(0.7, 10), lo, hi).mean().round(3))

# %% [markdown]
# **AI step.** Visualise the trade-off:
# ```
# Make one self-contained HTML page with two bar charts on one axis: heads in 10 flips for a fair coin and for a coin that lands heads 70% of the time. Let me move the rejection region, shade α and β, and show both numbers.
# ```
# If the page disagrees with the cell above, tell the AI exactly: "I set [this]. I expected [this], but got [that]."

# %% [markdown]
# **AI step.** Explain it. In a new chat, paste this first, then explain Type I and Type II errors in your own words, using the dealer's coin:
# ```
# I will explain Type I and Type II errors. Do not reply until I write DONE. Then tell me what is right, what is missing, and what is wrong, and ask me one question about the weakest part.
# ```

# %% [markdown]
# ## Optional: three harder questions
# Work each on paper first. To check an answer with the AI tutor, paste:
# ```
# I am learning [the question]. Here is my answer: [paste]. Do not give me the answer. Tell me what is right and wrong, then ask me one question at a time.
# ```

# %% [markdown]
# ### A. How many accused dealers are cheaters?
# 1 in 10 dealers cheats with the 70% coin.
#
# **Change:** 100 flips per dealer (`lo=39, hi=61`), or half the dealers cheating.

# %%
cheat = np.arange(runs) % 10 == 0
heads = (rng.random(size=(runs, 10)) < np.where(cheat, 0.7, 0.5)[:, None]).sum(axis=1)
accused = accuse(heads)
print("share of dealers accused:", accused.mean().round(3))
print("share of accused who cheat:", cheat[accused].mean().round(3))

# %% [markdown]
# ### B. Estimating the cheat from caught cheaters
# **Change:** 20 flips (`lo=5, hi=15`) and 100 flips (`lo=39, hi=61`).

# %%
heads = flips(0.7, 10)
caught = accuse(heads)
(heads[caught] / 10).mean()

# %% [markdown]
# ### C. Peeking
# **Change:** add a third look after 30 flips. What happens to the false-accusation rate?

# %%
first, second = flips(0.5, 10), flips(0.5, 10)
total = first + second
print("peek at 10, test again at 20:", (accuse(first) | accuse(total, 5, 15)).mean().round(3))
print("one test at 20 flips:", accuse(total, 5, 15).mean().round(3))
