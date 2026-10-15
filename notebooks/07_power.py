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
# # Power: how many mice does an experiment need?
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/07_power.ipynb)
#
# **Takeaway: simulating the planned experiment many times shows how many mice it needs to catch an effect worth finding.**
#
# This is the seventh notebook of the series and the first of Day 3.
# Notebook 5 computed how often the coin rule catches a cheating dealer: its power.
# Here you plan a mouse experiment before doing it: how many mice per group?
# Notebook 8 designs the rest of the experiment.
# Exercises marked *Stretch (optional)* can be skipped.
#
# Python practice: calling a function you write, once per simulated experiment, inside a loop.
#
# **Start here:** save your own copy with *File > Save a copy in Drive*, so your edits are kept.
# Switch off Colab's AI code completion for these exercises.
# Then run the cells in order with Shift+Enter (run and move to the next cell).
# Ctrl+Enter (Cmd+Enter on a Mac) reruns a cell without moving on.

# %%
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(20261007)  # one generator for the whole notebook, as in notebooks 1-3

# %% [markdown]
# ## The shuffle test of notebook 3, as a function
#
# In notebook 3 the ten lean mice sat in one array.
# Here the two groups come as two arrays, and `np.concatenate` joins them into one:

# %%
lean_control = np.array([543, 83, 555, 483, 557])  # tumor volumes (mm^3), control antibody
lean_treated = np.array([0, 70, 0, 257, 29])       # anti-PD-L1
print(np.concatenate([lean_control, lean_treated]))

# %% [markdown]
# The next cell wraps notebook 3's shuffle loop in a function that returns the p-value,
# so that one line tests any two groups.
# Two changes from notebook 3: it counts differences in both directions, as most papers do,
# and it uses 1000 shuffles instead of 10000, for speed.
# On the lean mice, each of notebook 3's 2 extreme splits (out of 252) has a mirror image with the sign flipped,
# so both directions give 4/252, about 0.016.

# %%
def shuffle_test(control, treated):
    values = np.concatenate([control, treated])
    k = len(control)
    observed = control.mean() - treated.mean()
    diffs = []
    for i in range(1000):
        shuffled = rng.permutation(values)
        diffs.append(shuffled[:k].mean() - shuffled[k:].mean())
    diffs = np.array(diffs)
    # "- 1e-9" keeps ties lost to rounding (notebook 3, "Why whole numbers?")
    return (np.abs(diffs) >= abs(observed) - 1e-9).mean()


print(shuffle_test(lean_control, lean_treated))

# %% [markdown]
# ## A drug that works, tested on five mice
#
# Mice learn to fear a cage where they once felt a mild foot shock:
# put back in it, they *freeze* (stand still except for breathing),
# and the fraction of time they freeze measures their fear memory.
# You plan to test whether a drug given right after training weakens that memory.
#
# Carneiro et al. (2018) collected 410 such experiments from 122 papers.
# In a typical one, control mice freeze about 50% of the time, with a standard deviation of about 17 percentage points between mice,
# and an effective drug lowers freezing to about 31%.
# Most used 8 to 12 mice per group.
#
# **Here we play nature: the simulation knows each group's true mean and standard deviation.
# A real lab only guesses them from earlier experiments like these.**
# Each simulated mouse is one draw from a bell curve, `rng.normal(mean, sd)`, as in notebook 2.

# %%
n = 5  # mice per group
control = rng.normal(50, 17, size=n)  # % of time freezing, control mice
treated = rng.normal(31, 17, size=n)  # % of time freezing, drug-treated mice
print(control.round(), treated.round())
print(shuffle_test(control, treated))

# %% [markdown]
# Run that cell again a few times with Ctrl+Enter.
# The drug works in every run: it lowers the true mean by 19 points.
# Does the test detect it (p at most 0.05) every time?
#
# <details>
# <summary>Answer</summary>
#
# No.
# The p-value jumps from run to run, from below 0.01 to above 0.5:
# five mice per group differ so much by chance that the drug's 19 points are sometimes hidden.
# Each run is one experiment you might have done.
#
# (A negative freezing time comes from the bell curve's tail, about 1 drug-treated mouse in 30;
# cutting the curve off at 0 barely changes the answers below.)
#
# </details>

# %% [markdown]
# ## How often does the test catch a drug that works?
#
# The next cell repeats the experiment 1000 times and keeps the 1000 p-values.
# That is a million shuffles; expect about 30 seconds in Colab.
#
# **Predict first:** out of 1000 experiments with 5 mice per group, how many detect the drug?
# Choose your answer in the menu on the right side of the next cell, then run that cell.

# %%
# Choose your prediction in the menu on the right of this cell, then run the cell.
# The menu rewrites the line below; do not edit it by hand.
prediction = "choose"  # @param ["choose", "almost all", "about two thirds", "about one third", "almost none"]

# %%
assert prediction != "choose", "Choose your prediction in the menu on the right of the cell above, then run that cell."

n = 5  # mice per group
experiments = 1000
p_values = []
for i in range(experiments):
    control = rng.normal(50, 17, size=n)
    treated = rng.normal(31, 17, size=n)
    p_values.append(shuffle_test(control, treated))
p_values = np.array(p_values)  # an array, so that one comparison checks every experiment at once
print(p_values[:10])  # the first ten experiments

# %% [markdown]
# Which of these ten experiments detected the drug?
# Compare them all with 0.05 at once, as notebook 1 compared every roll with 3.
# The rule is "p at most 0.05", so `<=`: with 1000 shuffles, p can be exactly 0.05.

# %%
print(p_values[:10] <= 0.05)

# %% [markdown]
# **Your turn:** replace the `...` with the fraction of all 1000 experiments with p at most 0.05, then run the cell.
# Compare every experiment as above, then take `.mean()`: each `True` counts as 1 and each `False` as 0.
# If you get stuck, open the answer below.

# %%
power = ...  # fraction of experiments with p at most 0.05
assert power is not Ellipsis, "Replace ... with the fraction of experiments with p at most 0.05. Open the answer below if you need help, then rerun this cell."
print(power)

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# ```python
# power = (p_values <= 0.05).mean()
# ```
#
# About 0.33, give or take a few hundredths from one set of 1000 experiments to the next.
# The drug works in every experiment, yet only about one in three detects it.
# Did you guess higher? So do researchers:
# 89% of 214 psychology researchers surveyed overestimated the power of small-effect designs (Bakker et al., 2016).
#
# So a p-value above 0.05 here never means that the drug does nothing;
# it means that this experiment did not detect it (Greenland et al., 2016).
# A p-value counts shuffles; this fraction counts experiments.
#
# </details>

# %% [markdown]
# ## More mice, more often
#
# The usual target is to detect the effect in 80% of experiments.
# The next cell repeats the loop for 5, 10, 15, 20, and 30 mice per group,
# with 500 experiments each to save time, and plots the fraction that detect the drug.
# It takes up to half a minute.
#
# **Predict first:** how many mice per group detect the drug in 80% of experiments?
# Choose your answer in the menu on the right side of the next cell, then run that cell.

# %%
# Choose your prediction in the menu on the right of this cell, then run the cell.
# The menu rewrites the line below; do not edit it by hand.
prediction_n = "choose"  # @param ["choose", "about 8", "about 15", "about 30", "about 60"]

# %%
assert prediction_n != "choose", "Choose your prediction in the menu on the right of the cell above, then run that cell."

n_values = [5, 10, 15, 20, 30]  # mice per group
powers = []
for n in n_values:
    p_values = []
    for i in range(500):
        control = rng.normal(50, 17, size=n)
        treated = rng.normal(31, 17, size=n)
        p_values.append(shuffle_test(control, treated))
    powers.append((np.array(p_values) <= 0.05).mean())
powers = np.array(powers)
print(powers.round(2))

plt.figure(figsize=(5, 3))
plt.plot(n_values, powers, marker="o")
plt.axhline(0.8, color="black", linestyle="--")  # the usual target
plt.ylim(0, 1)
plt.xlabel("mice per group")
plt.ylabel("fraction of experiments\nthat detect the drug")
plt.show()

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# About 15.
# The curve crosses 0.8 between 10 and 15 mice per group, near 14.
# The field's usual 8 to 12 mice detect a typical drug only about 55% to 75% of the time.
# Carneiro et al. (2018) reached the same estimate, about 15 per group,
# and found it in only 12.2% of the experiments they collected.
#
# The curve is a little bumpy: each point comes from only 500 experiments (the next section says how bumpy).
#
# </details>

# %% [markdown]
# ## Power is a probability over experiments you have not done
#
# **In your own words:** what did the simulation show?
# Say it to an imaginary classmate before opening the answer.
#
# <details>
# <summary>Answer</summary>
#
# A drug that really works is not detected in every experiment.
# With 5 mice per group the test detected it in about a third of the simulated experiments,
# with more mice in more of them, and with about 15 per group in 80% of them.
#
# </details>
#
# - **Power** is the probability that the test rejects the null hypothesis
#   when the effect is real and of a given size.
#   For a test that rejects when $p \le \alpha$,
#   with $n$ mice per group and a true difference $\delta$ between the group means,
#
#   $$\text{power}(\delta, n) = P_\delta(p \le \alpha) = E_\delta\big[\mathbf{1}\{p \le \alpha\}\big],$$
#
#   where $\mathbf{1}\{p \le \alpha\}$ is 1 for an experiment that rejects and 0 for one that does not,
#   and $P_\delta$ and $E_\delta$ are taken over repeated experiments with true difference $\delta$.
# - A **Type II error** is failing to reject a false null hypothesis; its probability is $\beta = 1 - \text{power}(\delta, n)$.
#   At $\delta = 0$, the same probability $P_0(p \le \alpha)$ is the Type I error rate, at most $\alpha$ (notebook 5).
# - Power is not one number: it depends on $\delta$, $n$, the spread $\sigma$, $\alpha$, and the test.
# - Your `power` line averaged $M = 1000$ zeros and ones, $\frac{1}{M}\sum_{m=1}^{M} \mathbf{1}\{p_m \le 0.05\}$:
#   a sample mean that estimates the expectation above.
#   As in notebook 2, its standard deviation is $\sqrt{\text{power}\,(1 - \text{power})/M}$,
#   at most 0.016 for $M = 1000$ and 0.022 for $M = 500$.
#
# **A rule of thumb.**
# For two groups, a two-sided test at $\alpha = 0.05$ with power 0.80,
# and normally distributed measurements with the same $\sigma$ in both groups,
#
# $$n \approx \frac{16\,\sigma^2}{\delta^2} \text{ mice per group}$$
#
# (Lehr's rule; van Belle, 2008, Section 2.1).
# Here $16 \times 17^2 / 19^2 \approx 12.8$;
# the simulation needed about 14, because the rule treats $\sigma$ as known.
# Halve the difference worth finding, and you need four times the mice:
# the spread of an average shrinks like $1/\sqrt{n}$ (notebook 2).
#
# **Sample-size planning** (a priori power analysis) fixes, before the experiment,
# the smallest difference worth finding, a spread from earlier experiments,
# $\alpha$ and one or both directions, the test, and a target power, usually 80% to 95%;
# the simulation, or the rule in the simplest case, then gives $n$.
# Reports of animal experiments are asked to explain how the sample size was determined (Percie du Sert et al., 2020).
#
# **Deeper reading:** van Belle's [*Statistical Rules of Thumb*](https://doi.org/10.1002/9780470377963) (through CF;
# [Chapter 2, "Sample Size", is free](http://www.vanbelle.org/chapters/webchapter2.pdf)) derives the rule;
# Lakens (2022) covers justifying a sample size, with and without power.

# %% [markdown]
# ## The obese mice of notebook 3, planned
#
# In notebook 3 (Sipe et al., 2022), the five obese control tumors ranged from 1759 to 4540 mm$^3$:
# a mean of about 2500 mm$^3$ and a standard deviation of about 1200 mm$^3$.
# Plan the next obese experiment, with 300 mm$^3$ (a tumor 12% smaller) as the smallest difference worth finding.
#
# **Predict first, from the rule of thumb:** how many mice per group?
# Write your number down, then run the next cell:
# it repeats the loop for 50 to 300 mice per group, 300 experiments each, and takes up to half a minute.

# %%
n_values = [50, 100, 200, 300]  # mice per group
powers = []
for n in n_values:
    p_values = []
    for i in range(300):
        control = rng.normal(2500, 1200, size=n)  # tumor volume (mm^3), control antibody
        treated = rng.normal(2200, 1200, size=n)  # anti-PD-L1, 300 mm^3 smaller
        p_values.append(shuffle_test(control, treated))
    powers.append((np.array(p_values) <= 0.05).mean())
powers = np.array(powers)
print(powers.round(2))

plt.figure(figsize=(5, 3))
plt.plot(n_values, powers, marker="o")
plt.axhline(0.8, color="black", linestyle="--")  # the usual target
plt.ylim(0, 1)
plt.xlabel("mice per group")
plt.ylabel("fraction of experiments\nthat detect the drug")
plt.show()

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# About 250 per group.
# The rule gives $16 \times 1200^2 / 300^2 = 256$, and the curve crosses 0.8 between 200 and 300.
# A 300 mm$^3$ difference is small next to tumors that differ by 1200 mm$^3$ from mouse to mouse.
#
# Two cautions.
# This is not "the power of notebook 3's experiment":
# power computed for a finished experiment, at the difference it happened to observe,
# only restates its p-value (Hoenig & Heisey, 2001). Power is for planning.
# And the 1200 comes from five mice, so a plan built on it is only as good as that guess (Lakens, 2022).
#
# </details>

# %% [markdown]
# ## You can now...
#
# plan how many mice an experiment needs:
# simulate the planned experiment with the smallest effect worth finding,
# run the test you will run, and raise the number of mice until it detects the effect often enough.
#
# **For your own experiments, learn [G\*Power](https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower)**:
# free, for Windows and macOS, no programming.
# Choose **A priori**, the test you will run, $\alpha$, the target power,
# and the effect size, which for a t-test is $d = \delta / \sigma$ (here $19/17 \approx 1.1$).
# [UCLA's worked example](https://stats.oarc.ucla.edu/other/gpower/power-analysis-for-two-group-independent-sample-t-test/)
# shows how its **Determine** button computes $d$ from assumed means and standard deviations.
# G\*Power plans a t-test (in Python: `statsmodels.stats.power.TTestIndPower`); to plan a shuffle test, simulate it as above.
#
# Small experiments that do reach $p \le 0.05$ overstate the effect, because only the lucky ones get there
# (the stretch below shows it), and they are common:
# the median power in neuroscience has been estimated at 21% (Button et al., 2013).
#
# ## Why plan?
#
# Power is the fraction of planned experiments that would catch the effect;
# choose the number of mice that makes it high.

# %% [markdown]
# ## Stretch (optional)
#
# > **Stretch (optional): lucky experiments exaggerate.**
# > In a new cell, repeat the 1000-experiment loop with 5 mice per group,
# > but also keep each experiment's observed difference, `control.mean() - treated.mean()`.
# > Average it over the experiments that detected the drug, and compare with the true difference, 19.
# > Then try 30 mice per group.
#
# <details>
# <summary>Answer</summary>
#
# ```python
# n = 5
# p_values = []
# observed = []
# for i in range(1000):
#     control = rng.normal(50, 17, size=n)
#     treated = rng.normal(31, 17, size=n)
#     p_values.append(shuffle_test(control, treated))
#     observed.append(control.mean() - treated.mean())
# p_values = np.array(p_values)
# observed = np.array(observed)
# print(observed[p_values <= 0.05].mean())
# ```
#
# About 29 with 5 mice per group, half again the true 19; about 19 or 20 with 30 mice per group.
# With 5 mice, only the experiments that happened to draw a large difference reach $p \le 0.05$,
# so the ones that detect the drug overstate its effect.
# This is the winner's curse of notebook 5's optional question, here in mice
# (Button et al., 2013; Gelman & Carlin, 2014).
#
# </details>

# %% [markdown]
# ## References
#
# Bakker, M., Hartgerink, C. H. J., Wicherts, J. M., & van der Maas, H. L. J. (2016).
# Researchers' intuitions about power in psychological research.
# *Psychological Science, 27*(8), 1069-1077. https://doi.org/10.1177/0956797616647519
#
# Button, K. S., Ioannidis, J. P. A., Mokrysz, C., Nosek, B. A., Flint, J., Robinson, E. S. J., & Munaf&ograve;, M. R. (2013).
# Power failure: Why small sample size undermines the reliability of neuroscience.
# *Nature Reviews Neuroscience, 14*(5), 365-376. https://doi.org/10.1038/nrn3475
#
# Carneiro, C. F. D., Moulin, T. C., Macleod, M. R., & Amaral, O. B. (2018).
# Effect size and statistical power in the rodent fear conditioning literature - A systematic review.
# *PLOS ONE, 13*(4), e0196258. https://doi.org/10.1371/journal.pone.0196258
#
# Gelman, A., & Carlin, J. (2014).
# Beyond power calculations: Assessing Type S (sign) and Type M (magnitude) errors.
# *Perspectives on Psychological Science, 9*(6), 641-651. https://doi.org/10.1177/1745691614551642
#
# Greenland, S., Senn, S. J., Rothman, K. J., Carlin, J. B., Poole, C., Goodman, S. N., & Altman, D. G. (2016).
# Statistical tests, P values, confidence intervals, and power: A guide to misinterpretations.
# *European Journal of Epidemiology, 31*(4), 337-350. https://doi.org/10.1007/s10654-016-0149-3
#
# Hoenig, J. M., & Heisey, D. M. (2001).
# The abuse of power: The pervasive fallacy of power calculations for data analysis.
# *The American Statistician, 55*(1), 19-24. https://doi.org/10.1198/000313001300339897
#
# Lakens, D. (2022). Sample size justification.
# *Collabra: Psychology, 8*(1), Article 33267. https://doi.org/10.1525/collabra.33267
#
# Percie du Sert, N., Ahluwalia, A., Alam, S., Avey, M. T., Baker, M., Browne, W. J., Clark, A., Cuthill, I. C., Dirnagl, U., Emerson, M., Garner, P., Holgate, S. T., Howells, D. W., Hurst, V., Karp, N. A., Lazic, S. E., Lidster, K., MacCallum, C. J., Macleod, M., ... W&uuml;rbel, H. (2020).
# Reporting animal research: Explanation and elaboration for the ARRIVE guidelines 2.0.
# *PLOS Biology, 18*(7), e3000411. https://doi.org/10.1371/journal.pbio.3000411
#
# Sipe, L. M., Chaib, M., Korba, E. B., Jo, H., Lovely, M. C., Counts, B. R., Tanveer, U., Holt, J. R., Clements, J. C., John, N. A., Daria, D., Marion, T. N., Bohm, M. S., Sekhri, R., Pingili, A. K., Teng, B., Carson, J. A., Hayes, D. N., Davis, M. J., ... Makowski, L. (2022).
# Response to immune checkpoint blockade improved in pre-clinical model of breast cancer after bariatric surgery.
# *eLife, 11*, e79143. https://doi.org/10.7554/eLife.79143
#
# van Belle, G. (2008). *Statistical rules of thumb* (2nd ed.). Wiley. https://doi.org/10.1002/9780470377963
