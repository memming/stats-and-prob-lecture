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
# # AI-assisted data analysis with real mice
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/06_real_data.ipynb)
#
# **Takeaway: the AI can do every step fast; you decide what to test, what counts as one observation, and you check each step.**
# Data: BDNF protein in mouse cortex from a Down syndrome mouse model, as a messy lab export (Higuera, Gardiner & Cios 2015, PLoS ONE; UCI, CC BY 4.0).
# Steps: 0 vibe research, 1 clean the files, 2 look at the data, 3 your hypothesis, 4 test it, 5 show the result.
# At each step the AI writes the code; you paste it into the empty cell, run it, and check it.
#
# **Start here:** save your own copy with *File > Save a copy in Drive*, so your edits are kept.

# %% [markdown]
# **AI step.** **Step 0 — vibe research (the baseline).** Download `bdnf_raw.zip` (link below), upload it to your AI chat, and paste:
# ```
# Analyse this data and tell me what it shows.
# ```
# Copy its main claim into the next cell. You will compare it with your own analysis at the end.

# %% [markdown]
# *The AI's main claim:*

# %% [markdown]
# ## Load the files
# Run the next cell. It downloads `bdnf_raw.zip` from the course repository, unzips it, and shows the README and the first lines of every file. [Download the zip](https://github.com/memming/stats-and-prob-lecture/raw/main/data/bdnf_raw.zip) for step 0.

# %%
import io, pathlib, urllib.request, zipfile

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if not pathlib.Path("bdnf_raw").exists():
    if pathlib.Path("bdnf_raw.zip").exists():  # downloaded already, or uploaded to Colab
        zipfile.ZipFile("bdnf_raw.zip").extractall()
    else:
        url = "https://github.com/memming/stats-and-prob-lecture/raw/main/data/bdnf_raw.zip"
        zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url).read())).extractall()
print(pathlib.Path("bdnf_raw/README.txt").read_text())
for f in sorted(pathlib.Path("bdnf_raw").glob("*_*")):
    print("=====", f.name)
    if f.suffix == ".xlsx":
        print(pd.read_excel(f).head(3).to_string())
    else:
        print("\n".join(f.read_text().splitlines()[:3])[:400])

# %% [markdown]
# ## Step 1 — clean the files with AI
# Paste the README and the output above into your AI chat, with:
# ```
# Write pandas code that reads all these files into one long table called d, with columns mouse_id, genotype, treatment, learning, reading, BDNF (one row per reading). Missing readings must become NaN. List every problem in the files that your code handles. The files are in the folder bdnf_raw.
# ```
# Paste the code into the next cell and run it.

# %%
# Paste the AI's code here. It must create the table d.

# %% [markdown]
# **Check.** Run the next cell. Do the numbers match the README? If not, tell the AI exactly:
# "I ran [this]. I expected [this], but got [that]."

# %%
if "d" in globals():
    print("mice:", d.mouse_id.nunique(), "| rows:", len(d), "| missing BDNF:", d.BDNF.isna().sum())
    print("readings per mouse:", d.groupby("mouse_id").size().value_counts().to_dict())
    print(d.groupby(["genotype", "treatment", "learning"]).mouse_id.nunique())
else:
    print("Run your step 1 code first: it must create the table d.")


# %% [markdown]
# ## Step 2 — look at the data
# Ask the AI:
# ```
# Write matplotlib code for the table d: one column of points per group (genotype, treatment, learning). Show each mouse's 15 readings as small dots and the mouse's mean as a larger dot.
# ```
# Paste and run it.

# %%
# Paste the AI's plotting code here.

# %% [markdown]
# **Look.** Do the 15 readings of one mouse sit together? Which groups look different from each other? What counts as one observation here: a reading or a mouse?

# %% [markdown]
# *Your notes:*

# %% [markdown]
# ## Step 3 — your hypothesis (AI closed first)
# From what you saw, write one hypothesis to test: the two groups you compare, the null hypothesis, what counts as one observation, the statistic, and your prediction.
# Then ask the AI to attack it:
# ```
# Here is my analysis plan: [paste]. Find the weakest point. Do not write code.
# ```

# %% [markdown]
# *Your plan:*

# %% [markdown]
# ## Step 4 — test it
# Ask the AI:
# ```
# Write a Python function my_test(a, b) that returns the two-sided permutation p-value for the difference in means of the arrays a and b, with 2000 shuffles. Then write code that applies it to my plan: [paste your plan], using the table d.
# ```
# Paste and run it.

# %%
# Paste the AI's test code here. It must define my_test(a, b).

# %% [markdown]
# **Check the test on fake groups.** The next cell splits the saline-treated Control mice at random into two fake groups, 200 times, and runs your `my_test` on each split, once with one mean per mouse and once with every reading counted separately.
# Nothing differs between fake groups, so a good test calls about 5% of them significant. Predict both rates first.

# %%
def false_positive_rate(test, level, n_splits=200, seed=1):
    rng = np.random.default_rng(seed)
    sal = d[(d.genotype == "Control") & (d.treatment == "Saline")].dropna(subset=["BDNF"])
    mice = sal.mouse_id.unique()
    hits = 0
    for _ in range(n_splits):
        group = set(rng.permutation(mice)[: len(mice) // 2])
        in_a = sal.mouse_id.isin(group)
        if level == "mouse":
            means = sal.groupby("mouse_id").BDNF.mean()
            a, b = means[means.index.isin(group)].to_numpy(), means[~means.index.isin(group)].to_numpy()
        else:
            a, b = sal.BDNF[in_a].to_numpy(), sal.BDNF[~in_a].to_numpy()
        hits += test(a, b) < 0.05
    return hits / n_splits


if "my_test" in globals() and "d" in globals():
    for level in ["mouse", "reading"]:
        print(level, "level: false-positive rate", false_positive_rate(my_test, level))
else:
    print("Run steps 1 and 4 first: they must create d and my_test.")

# %% [markdown]
# ## Step 5 — show the result
# Ask the AI:
# ```
# Write matplotlib code that shows my result: one dot per mouse for the two groups I compared, the group means, and next to it a histogram of the shuffled differences with a line at the observed difference.
# ```
# Paste and run it.

# %%
# Paste the AI's result plot here.

# %% [markdown]
# **AI step.** Write two sentences on what your result means. Then paste:
# ```
# Here is my conclusion: [paste]. Act as a critical reviewer. Find the weakest claim and ask me to fix it. Do not rewrite it.
# ```
# Finally, compare with step 0: where did the vibe-research answer and your analysis differ? Which do you trust, and why?

# %% [markdown]
# *Your conclusion, and the comparison with step 0:*
