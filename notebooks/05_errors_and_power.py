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
# # The dealer's coin: how often does a good rule get it wrong?
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/05_errors_and_power.ipynb)
#
# **Takeaway: the rule sets how often you accuse an honest dealer; how often you catch a cheater depends on the cheat, and only more data makes it easy.**
# This morning you invented a rule: watch 10 flips, and accuse the dealer if there are 0, 1, 9, or 10 heads.
# Each part: work it out first with AI closed, then do the **AI step**. Part 5 checks your answers with code.
#
# **Start here:** save your own copy with *File > Save a copy in Drive*, so your edits are kept.

# %% [markdown]
# ## Part 1 — How often does the rule accuse an honest dealer?
# Heads in 10 flips of a fair coin:
#
# | Heads | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
# |---|---|---|---|---|---|---|---|---|---|---|---|
# | P | 0.001 | 0.010 | 0.044 | 0.117 | 0.205 | 0.246 | 0.205 | 0.117 | 0.044 | 0.010 | 0.001 |
#
# 1. The dealer is honest. How often does your rule accuse them?

# %% [markdown]
# *Your answer:*

# %% [markdown]
# ## Part 2 — Two types of error, and the power curve
# 2. Fill in the table. Which two cells are mistakes? Which one did you just compute? **Predict:** can the other mistake be one number, like 0.022? Write yes or no.
#
# |               | Dealer is honest | Dealer cheats |
# |---------------|------------------|---------------|
# | Accuse        |                  |               |
# | Do not accuse |                  |               |
#
# 3. The dealer's coin lands heads 70% of the time. Heads in 10 flips of this coin:
#
# | Heads | 0–2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
# |---|---|---|---|---|---|---|---|---|---|
# | P | 0.002 | 0.009 | 0.037 | 0.103 | 0.200 | 0.267 | 0.233 | 0.121 | 0.028 |
#
# How often does your rule accuse this cheater? How often does the cheater get away?
#
# 4. Your group computes P(accuse) for one more coin: 60%, 80%, or 90% heads. Use P(9 heads) = 10 · p⁹ · (1 − p) and P(10 heads) = p¹⁰ (0 and 1 heads are tiny). Sketch P(accuse) against how often the coin lands heads. Where does the curve start?

# %% [markdown]
# *Your answer:*

# %% [markdown]
# 4b. Can the Type II error rate of your rule be one number? Write your idea.
#
# *Your answer:*

# %% [markdown]
# **AI step.** Can the Type II error rate of your rule be one number? Write your idea in the answer cell first, then ask the AI tutor:
# ```
# My rule: flip 10 times, accuse on 0, 1, 9 or 10 heads. The chance of catching a cheater is 0.048 (60% coin), 0.15 (70%), 0.38 (80%), 0.74 (90%). Can its Type II error rate be one number? My idea: [your idea]. Do not give me the answer; ask me one question at a time.
# ```

# %% [markdown]
# ## Part 3 — Reading the power curve, and the trade-off between α and β
# 5. Put the class's numbers together: P(accuse) for coins with 50%, 60%, 70%, 80%, 90%, and 100% heads. Where does the curve start, and why there? How biased must the coin be before your rule catches it more often than not? What new idea did the AI tutor give you in Part 2?

# %% [markdown]
# *Your answer:*

# %% [markdown]
# **AI step.** Visualise the power curve. Ask for:
# ```
# Make one self-contained HTML page that plots the power curve of this rule (flip 10 times, accuse on 0, 1, 9, or 10 heads): the chance of accusing against how often the coin lands heads, with a slider for the number of flips.
# ```
# Check it: at 50% heads it must show 0.022, and at 70% about 0.15. How does the curve change with 20, 50, and 100 flips?

# %% [markdown]
# 6. Change the rule: accuse on 0, 1, 2, 8, 9, or 10 heads. Compute the new chance of accusing an honest dealer and of catching the 70% cheater. What did you gain, and what did you pay?

# %% [markdown]
# *Your answer:*

# %% [markdown]
# **AI step.** Visualise the trade-off. Ask for:
# ```
# Make one self-contained HTML page with two bar charts on one axis: heads in 10 flips for a fair coin and for a coin that lands heads 70% of the time. Let me move the rejection region, shade α and β, and show both numbers.
# ```
# Check it against your answers to questions 1, 3, and 6. If it is wrong, tell it exactly: "I set [this]. I expected [this], but got [that]."

# %% [markdown]
# **AI step.** Explain it. In a new chat, explain Type I and Type II errors to the AI in your own words, using the dealer's coin. Paste first:
# ```
# I will explain Type I and Type II errors. Do not reply until I write DONE. Then tell me what is right, what is missing, and what is wrong, and ask me one question about the weakest part.
# ```
# Was your prediction in question 2 right?

# %% [markdown]
# *Your answer:*

# %% [markdown]
# ## Part 4 (optional) — Three questions, three groups
# If time allows. Your group takes one question.
#
# **Steps.** 1. Work it out on paper, AI closed (5 minutes). 2. Check it with the AI tutor below (5 minutes). 3. Explain it to the class without notes (2 minutes): say the answer, how you got it, and what it means for research.
#
# **Group A — How many accused dealers are cheaters?**
# In this casino, 1 in 10 dealers cheats with the 70% coin. You watch 10 flips of each of 1,000 dealers and use your rule.
# - Fill in the table: how many honest dealers do you accuse, and how many cheaters?
#
# |             | Honest dealers (900) | Cheating dealers (100) |
# |-------------|----------------------|------------------------|
# | Accused     |                      |                        |
# | Not accused |                      |                        |
#
# - Of the accused dealers, what fraction cheat?
# - The manager says: "We accused 35 of 1,000 dealers. That is 3.5%, less than 0.05, so this casino has no cheating problem." Is the manager right?
# - Redo the fraction with 100 flips per dealer (accuse on ≤ 39 or ≥ 61 heads: α = 0.035, power = 0.98), and again for a casino where half the dealers cheat (10 flips). Which change raises the fraction more?
# - *Explain to the class:* why "p < 0.05" does not mean "95% sure the effect is real".
#
# **Group B — Estimating the cheat from caught cheaters**
# With 10 flips your rule catches the 70% coin only when it shows 9 or 10 heads. The rule changes with the number of flips, to keep α below 0.05: accuse on ≤ 5 or ≥ 15 heads with 20 flips, and on ≤ 39 or ≥ 61 heads with 100 flips.
# - Among the cheaters you catch with 10 flips, what is the average heads rate? Use P(9) = 0.121 and P(10) = 0.028. Compare it with the true 0.70.
# - Predict the average with 20 and with 100 flips.
# - *Explain to the class:* why a small study that finds an effect usually overestimates it.
#
# **Group C — Peeking**
# You watch 10 flips. If you cannot accuse, you watch 10 more and accuse if all 20 flips show 5 or fewer, or 15 or more heads. Each test alone keeps α below 0.05.
# - Can the chance of accusing an honest dealer be smaller than 0.022? Estimate it: is it still below 0.05?
# - What happens if you keep adding 10 flips until you can accuse?
# - *Explain to the class:* why "add mice until p < 0.05" is not allowed.

# %% [markdown]
# *Your answer:*

# %% [markdown]
# **AI step.** Check and go deeper with the AI tutor:
# ```
# I am learning [your group's question]. Here is my answer: [paste]. Do not give me the answer. Tell me what is right and what is wrong, then ask me one question at a time.
# ```

# %% [markdown]
# ## Part 5 — Check with code
# Run each cell only after you have written your answer. `runs` games, one row per game, as this morning.

# %%
import numpy as np

rng = np.random.default_rng(20261005)
runs = 100000


def accuse(heads):
    return (heads <= 1) | (heads >= 9)


# %% [markdown]
# ### Question 1: an honest dealer is sometimes accused
#
# <details><summary>Answer</summary>
#
# About 0.022: the probability of 0, 1, 9, or 10 heads with a fair coin. This is the Type I error rate of the rule.
#
# </details>

# %%
heads = rng.integers(0, 2, size=(runs, 10)).sum(axis=1)
accuse(heads).mean()

# %% [markdown]
# ### Questions 3–4: the power curve
# `rng.random(size=(runs, 10)) < p` makes a coin that lands heads with probability `p`.
#
# <details><summary>Answer</summary>
#
# P(accuse) = 0.022 at 50% (that is α), 0.048 at 60%, 0.15 at 70%, 0.38 at 80%, 0.74 at 90%. The Type II error rate 1 − P(accuse) changes with the cheat, so there is no single Type II error rate: report it at the smallest cheat you care about, or show the whole curve.
#
# </details>

# %%
for p in [0.5, 0.6, 0.7, 0.8, 0.9]:
    heads = (rng.random(size=(runs, 10)) < p).sum(axis=1)
    print(p, accuse(heads).mean().round(3))

# %% [markdown]
# ### Question 5: more flips, a steeper curve
#
# <details><summary>Answer</summary>
#
# With 10 flips the rule catches the 70% coin 15% of the time; with 20 flips (accuse on ≤ 5 or ≥ 15 heads) 42%; with 50 flips (≤ 17 or ≥ 33) 78%. The false-accusation rate stays below 0.05 (0.022, 0.041, 0.033). More flips make the curve steeper, so smaller cheats become catchable.
#
# </details>

# %%
for n, lo, hi in [(10, 1, 9), (20, 5, 15), (50, 17, 33)]:
    fair = rng.integers(0, 2, size=(runs, n)).sum(axis=1)
    cheat = (rng.random(size=(runs, n)) < 0.7).sum(axis=1)
    print(n, "flips: alpha", ((fair <= lo) | (fair >= hi)).mean().round(3), "power", ((cheat <= lo) | (cheat >= hi)).mean().round(3))

# %% [markdown]
# ### Question 6: the trade-off
# **Tweak:** change the rule in `accuse` to `heads <= 2` or `heads >= 8`, then rerun the cells for questions 1 and 3–4.
#
# <details><summary>Answer</summary>
#
# α rises from 0.022 to 0.109; power against the 70% coin rises from 0.15 to 0.38. Moving the rule trades α against β; only more flips lower both.
#
# </details>

# %% [markdown]
# ### Group A: who is accused?
#
# <details><summary>Answer</summary>
#
# About 20 honest and 15 cheating dealers are accused, so only about 43% of accused dealers cheat. The manager is wrong: 3.5% is not a p-value; if every dealer were honest the rule would accuse about 1,000 × 0.022 = 22, and 35 or more has probability about 0.006, so some dealers cheat. With 100 flips, 76% of the accused cheat; with half the dealers cheating, 87%.
#
# </details>

# %%
cheat = np.arange(runs) % 10 == 0
p_heads = np.where(cheat, 0.7, 0.5)
heads = (rng.random(size=(runs, 10)) < p_heads[:, None]).sum(axis=1)
cheat[accuse(heads)].mean()

# %% [markdown]
# ### Group B: caught cheaters look worse than they are
#
# <details><summary>Answer</summary>
#
# About 0.92 with 10 flips, although the true rate is 0.70. Only extreme samples pass the rule, so significant results exaggerate the effect (the winner's curse).
#
# </details>

# %%
heads = (rng.random(size=(runs, 10)) < 0.7).sum(axis=1)
(heads[accuse(heads)] / 10).mean()

# %% [markdown]
# ### Group C: peeking
#
# <details><summary>Answer</summary>
#
# About 0.054: 0.022 at 10 flips plus 0.033 more at 20. Each test alone is below 0.05, but looking twice is not. Adding flips (or mice) until you can accuse keeps raising it.
#
# </details>

# %%
flips = rng.integers(0, 2, size=(runs, 20))
first = flips[:, :10].sum(axis=1)
total = flips.sum(axis=1)
(accuse(first) | (total <= 5) | (total >= 15)).mean()
