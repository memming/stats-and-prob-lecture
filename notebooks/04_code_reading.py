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
# # Reading code with AI: your morning test and an AI version
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/04_code_reading.ipynb)
#
# **Takeaway: you understand a test's code when you can predict what a change will do before you run it.**
# This builds on this morning's "Implement your own hypothesis test". The prompts to paste are in the boxes below.
#
# **Start here:** save your own copy with *File > Save a copy in Drive*, so your edits are kept.

# %%
import numpy as np

rng = np.random.default_rng(20261005)

# %% [markdown]
# ## Part A — your morning code
# Paste the hypothesis test you wrote this morning into the next cell, and run it.

# %%
# Paste your morning hypothesis test here.

# %% [markdown]
# ## Run it on a case you can check by hand
# **Predict first:** pick a small case where you know the answer.
# - Coin test: 9 heads in 10 flips. What is the two-sided p-value? (Use the worksheet table.)
# - Tumor volumes from this morning's notebook 3 (lean mice, whole mm³): control 543, 83, 555, 483, 557; anti-PD-L1 0, 70, 0, 257, 29. There are 252 ways to split the ten mice into two groups of five. What was the exact two-sided p-value this morning?
#
# Then run your code on it. Same answer?

# %% [markdown]
# ## Let the AI review it, without fixing it
# A fix gives you working code but not the reason it was wrong. Ask for a review instead.
#
# **1. Review.** Paste this, then your code:
# ```
# Do not rewrite or fix this code. First, tell me in one sentence what null hypothesis it tests. I will check whether that is what I meant. Then ask me up to 3 questions about the parts I should check.
# ```
# Compare its sentence with what you meant to test. If they differ, that is your bug.
#
# **2. Suspect a bug?** Paste:
# ```
# I ran [this]. I expected [this], but got [that]. Do not fix it and do not write code. Ask me one question that helps me find the problem myself.
# ```
#
# **3. Quiz.** Paste:
# ```
# Ask me 3 questions that test whether I understand this code: one about what a line does, one about why it is needed, and one about what would happen if I changed it. Ask one at a time and grade each answer. Do not show the answers.
# ```
# Write down your score.

# %% [markdown]
# ## Part B — an AI version
# This is real AI output (Claude Sonnet, 5 October 2026) for the prompt "Write a Python function that tests whether two groups differ, using a permutation (shuffle) test, and returns the p-value." It is longer than your code.
# **Predict first:** from the function name, inputs, and last line only, what does it do that yours does not?

# %%
# AI-generated code, kept exactly as produced. Model: Claude Sonnet (claude -p, alias "sonnet"), 5 October 2026.
# Prompt: "Write a Python function that tests whether two groups differ, using a permutation (shuffle) test,
# and returns the p-value. Use numpy. Give only the code, with a short example at the bottom."
# Use this file only if your own AI code does not work. Your task is to READ it, not to trust it.

import numpy as np


def permutation_test(a, b, n_permutations=10_000, statistic=None,
                     alternative="two-sided", seed=None):
    """
    Permutation (shuffle) test for a difference between two groups.

    Parameters
    ----------
    a, b : array-like
        Samples from the two groups.
    n_permutations : int
        Number of random shuffles.
    statistic : callable or None
        Function f(x, y) -> float. Defaults to difference in means.
    alternative : {"two-sided", "greater", "less"}
        "greater" tests mean(a) > mean(b); "less" tests mean(a) < mean(b).
    seed : int or None
        Seed for reproducibility.

    Returns
    -------
    p_value : float
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    rng = np.random.default_rng(seed)

    if statistic is None:
        statistic = lambda x, y: x.mean() - y.mean()

    observed = statistic(a, b)
    pooled = np.concatenate([a, b])
    n_a = len(a)

    perm_stats = np.empty(n_permutations)
    for i in range(n_permutations):
        shuffled = rng.permutation(pooled)
        perm_stats[i] = statistic(shuffled[:n_a], shuffled[n_a:])

    if alternative == "two-sided":
        count = np.sum(np.abs(perm_stats) >= abs(observed))
    elif alternative == "greater":
        count = np.sum(perm_stats >= observed)
    elif alternative == "less":
        count = np.sum(perm_stats <= observed)
    else:
        raise ValueError("alternative must be 'two-sided', 'greater', or 'less'")

    # +1 correction: the observed labeling is itself one valid permutation,
    # so the p-value is never exactly 0
    return (count + 1) / (n_permutations + 1)


# %%
a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])
permutation_test(a, b, n_permutations=9999, seed=0)

# %% [markdown]
# ## One-sided: which direction?
# **Predict:** read the docstring. Which group does `alternative="less"` say is smaller? What p do you expect for `"less"`, and for `"greater"`?

# %%
permutation_test(a, b, n_permutations=9999, seed=0, alternative="less")

# %% [markdown]
# ## Few shuffles: a noisy p-value
# **Tweak and observe:** change `n_permutations` from 9999 to 20, and rerun with `seed=1`, `seed=2`, `seed=3`. How much does p move?

# %%
permutation_test(a, b, n_permutations=9999, seed=1)

# %% [markdown]
# ## When the AI's code is wrong, say exactly how
# "It doesn't work" gives the AI nothing to check. Give it what you did, what you expected, and what you got:
# ```
# I ran [this]. I expected [this], but got [that]. That is wrong because [reason].
# ```
# The reason is the important part: if you cannot write it, you do not yet know that the code is wrong.

# %% [markdown]
# ## Why the "+ 1"?
# **Predict:** find the last line of the function. When could the p-value be exactly 0 without the `+ 1`? Is p = 0 ever a sensible answer?

# %% [markdown]
# ## Explain it, then let the AI test you
# **Three levels.** Paste, then the code:
# ```
# Explain this code three times: for a 5-year-old, an undergraduate, and a PhD student. At the PhD level, state the null hypothesis it tests and the assumptions it makes about the data.
# ```
#
# **A visual page.** Paste, then the code:
# ```
# Make one self-contained HTML page (no internet, no libraries) that shows what this code does: draw the two groups as dots, animate one shuffle, and build the histogram of shuffled differences step by step, with a line at the observed difference.
# ```
#
# **Quiz.** Use the quiz prompt from Part A on this AI code. Answer without looking at the code, and record your score.
