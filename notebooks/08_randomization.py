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
# # Randomization: let chance decide who gets the drug
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/08_randomization.ipynb)
#
# **Takeaway: assigning the drug at random keeps a hidden difference between mice from posing as a drug effect.**
#
# This is the eighth notebook of the series and the second of Day 3.
# Notebook 7 planned how many mice an experiment needs.
# This one plans who gets the drug and who knows it,
# then writes the design down in the form an animal-experiment approval asks for.
# Exercises marked *Stretch (optional)* can be skipped.
#
# Python practice: shuffling a list of group labels with `rng.permutation`, and picking out a group's values with a comparison.
#
# **Start here:** save your own copy with *File > Save a copy in Drive*, so your edits are kept.
# Switch off Colab's AI code completion for these exercises.
# Then run the cells in order with Shift+Enter (run and move to the next cell).
# Ctrl+Enter (Cmd+Enter on a Mac) reruns a cell without moving on.

# %%
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(20261007)  # one generator for the whole notebook, as in notebooks 1-7


# notebook 7's shuffle test, unchanged: the two-sided p-value for the difference in group means
def shuffle_test(control, treated):
    values = np.concatenate([control, treated])
    k = len(control)
    observed = control.mean() - treated.mean()
    diffs = []
    for i in range(1000):
        shuffled = rng.permutation(values)
        diffs.append(shuffled[:k].mean() - shuffled[k:].mean())
    diffs = np.array(diffs)
    # both directions; "- 1e-9" counts ties despite rounding in decimals (notebook 3, "Why whole numbers?")
    return (np.abs(diffs) >= abs(observed) - 1e-9).mean()


# %% [markdown]
# ## Mice taken out of the cage later are warmer
#
# You plan to test whether a new drug lowers body temperature.
# You will take the mice out of their home cages one at a time, inject them,
# and measure each one's rectal temperature.
#
# Takao et al. (2016) measured about 1700 mice this way.
# In a cage of four, the first mouse taken out was at about 36.1 C, the second 36.45, the third 36.7, the fourth 36.8:
# each removal disturbs the mice still waiting in the cage, and disturbed mice warm up.
# Individual mice vary around these values with a standard deviation of about 0.8 C.
#
# `np.tile` repeats a list.
# Here it lays out the four typical temperatures for five cages of four mice, in the order the mice are caught:

# %%
print(np.tile([36.1, 36.45, 36.7, 36.8], 5))

# %% [markdown]
# **Here we play nature: the simulation knows that the order of catching matters, and that the drug does nothing.
# A real lab sees only the 20 temperatures.**

# %%
cages = 5
typical = np.tile([36.1, 36.45, 36.7, 36.8], cages)        # typical temperature (C) by catch position, cage by cage
temperature = typical + rng.normal(0, 0.8, size=4 * cages)  # one experiment; the drug does nothing
print(temperature.round(1))

# %% [markdown]
# ## First caught, first treated
#
# The quickest allocation: in each cage, the first two mice you catch get the drug,
# and the last two get a saline injection, the control.
# As labels, in catch order:

# %%
labels = np.tile(["drug", "drug", "control", "control"], cages)  # first two caught in each cage get the drug
print(labels)

# %% [markdown]
# Comparing the labels with a word gives one `True` or `False` per mouse, as `rolls == 3` did in notebook 1:

# %%
print(labels == "drug")

# %% [markdown]
# Put inside `temperature[...]`, that comparison keeps the temperatures where it is `True`: the drug group.
# The last line tests one experiment:

# %%
group = labels
print(temperature[group == "drug"].round(1))
print(temperature[group == "control"].round(1))
print(shuffle_test(temperature[group == "control"], temperature[group == "drug"]))

# %% [markdown]
# One experiment, one p-value.
# (A printed 0.0 means that none of the 1000 shuffles did as well:
# p is below 1/1000, never exactly 0, as notebook 3 said.)
# The drug does nothing, so a fair test should call it significant only about 5% of the time,
# as in notebook 7's check.

# %% [markdown]
# ## How often does this experiment find a useless drug?
#
# The next cell repeats this experiment 1000 times.
# It keeps each p-value and each estimated drug effect (the drug group's mean minus the control group's),
# and draws a histogram of the estimated effects, with a black line at the true effect, zero.
# It takes a few seconds.
#
# **Predict first:** how often will the test call this useless drug significant?
# Choose your answer in the menu on the right side of the next cell, then run that cell.

# %%
# Choose your prediction in the menu on the right of this cell, then run the cell.
# The menu rewrites the line below; do not edit it by hand.
prediction = "choose"  # @param ["choose", "about 5%, as in notebook 7", "about 20%", "about 50%", "almost always"]

# %%
assert prediction != "choose", "Choose your prediction in the menu on the right of the cell above, then run that cell."

p_values = []
effects = []  # drug minus control (C)
for i in range(1000):
    temperature = typical + rng.normal(0, 0.8, size=4 * cages)
    group = labels  # first two caught in each cage get the drug
    p_values.append(shuffle_test(temperature[group == "control"], temperature[group == "drug"]))
    effects.append(temperature[group == "drug"].mean() - temperature[group == "control"].mean())
p_values = np.array(p_values)
print("fraction with p at most 0.05:", (p_values <= 0.05).mean())

plt.figure(figsize=(5, 3))
plt.hist(effects, bins=30, range=(-1.5, 1.5), edgecolor="white")
plt.axvline(0, color="black")  # the true effect of the drug: none
plt.xlabel("estimated drug effect, drug minus control (C)")
plt.ylabel("number of experiments")
plt.show()

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# About 20%, four times the 5% a fair test allows.
# The histogram is not centered on 0.
# The drug group holds the first and second mice caught in each cage, typically (36.1 + 36.45) / 2 = 36.275 C;
# the control group holds the third and fourth, typically (36.7 + 36.8) / 2 = 36.75 C.
# So the histogram centers on 36.275 - 36.75 = -0.475 C,
# and in most experiments the "drug" group comes out cooler.
#
# The test is not fooled: the groups really do differ, before any injection.
# The mistake is crediting the drug.
#
# </details>

# %% [markdown]
# ## Let chance decide who gets the drug
#
# **Your turn:** in the next cell, replace the `...` with a random assignment:
# shuffle `labels` with `rng.permutation`, as notebook 3 shuffled tumor volumes.
# The rest of the cell is the loop above.
# If you get stuck, open the answer below, replace `...`, and rerun the cell.

# %%
p_values = []
effects = []
for i in range(1000):
    temperature = typical + rng.normal(0, 0.8, size=4 * cages)
    group = ...  # random assignment: shuffle the labels before the experiment
    assert group is not Ellipsis, "Replace ... with the random assignment. Open the answer below if you need help, then rerun this cell."
    p_values.append(shuffle_test(temperature[group == "control"], temperature[group == "drug"]))
    effects.append(temperature[group == "drug"].mean() - temperature[group == "control"].mean())
p_values = np.array(p_values)
print("fraction with p at most 0.05:", (p_values <= 0.05).mean())

plt.figure(figsize=(5, 3))
plt.hist(effects, bins=30, range=(-1.5, 1.5), edgecolor="white")
plt.axvline(0, color="black")  # the true effect of the drug: none
plt.xlabel("estimated drug effect, drug minus control (C)")
plt.ylabel("number of experiments")
plt.show()

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# ```python
# group = rng.permutation(labels)
# ```
#
# About 5%, and the histogram is centered on 0.
# The same mice, the same useless drug, the same test;
# only the way the labels were handed out changed.
#
# </details>
#
# **Look at one random assignment.**
# The next cell prints the average catch position of each group (1 = caught first, 4 = caught last).
# **No real lab sees this; only the simulation knows the catch order.**
# Are the two groups equal?

# %%
position = np.tile([1, 2, 3, 4], cages)  # catch position of each mouse
group = rng.permutation(labels)
print("drug:", position[group == "drug"].mean(), " control:", position[group == "control"].mean())

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# Usually not exactly, and the gap changes each time you rerun the cell, now one way, now the other.
# Over many assignments the differences average out,
# and the shuffle test allows for exactly this chance:
# the about 5% of randomized experiments that reject are the draws that happened to be unbalanced.
#
# </details>

# %% [markdown]
# ## More mice shrink the noise, not the offset
#
# The next cell runs both allocations, first caught and random, for the number of cages set in its first line,
# and prints how often each calls the useless drug significant.
# Run it as it is (5 cages, 10 mice per group), then change `cages = 5` to `cages = 10` and run it again.
#
# **Predict first:** with 20 mice per group, will the first-caught allocation find the useless drug more often or less often?
# And random assignment?

# %%
cages = 5  # this cell sets its own number of cages
typical = np.tile([36.1, 36.45, 36.7, 36.8], cages)
labels = np.tile(["drug", "drug", "control", "control"], cages)

for allocation in ["first caught", "random"]:
    p_values = []
    for i in range(1000):
        temperature = typical + rng.normal(0, 0.8, size=4 * cages)
        if allocation == "first caught":
            group = labels
        else:
            group = rng.permutation(labels)
        p_values.append(shuffle_test(temperature[group == "control"], temperature[group == "drug"]))
    print(allocation, (np.array(p_values) <= 0.05).mean())

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# First caught: more often, about 45% with 10 cages against about 20% with 5.
# Random: about 5% both times.
# More mice shrink the noise around each estimate but not the first-caught allocation's false offset,
# so the offset stands out more clearly.
# No number of mice repairs a biased allocation.
#
# </details>

# %% [markdown]
# ## Randomization makes the shuffle test fair
#
# **In your own words:** what did the simulation show?
# Say it to an imaginary classmate before opening the answer.
#
# <details>
# <summary>Answer</summary>
#
# When the first-caught mice got the drug, a useless drug looked like it lowered temperature,
# about one experiment in five, and more often with more mice,
# because the drug group held the mice that were cooler anyway.
# When chance decided who got the drug, the test called it significant about 5% of the time, as it should.
#
# </details>
#
# - A **confounder** is a difference between the groups, other than the treatment, that affects the outcome:
#   here, the order of catching.
#   Giving the drug to the first mice caught made the comparison **biased**:
#   off in the same direction in every experiment, which more mice do not cure.
# - **Randomization** (random assignment): chance decides which mouse gets which treatment,
#   with the group sizes fixed. `rng.permutation(labels)` does exactly that.
# - Why it works: if the drug does nothing, each mouse's temperature is what it would have been under either label,
#   and the only random thing left is which labels the mice got.
#   The shuffle test repeats that random assignment, so it calls a useless drug significant at most 5% of the time,
#   whatever else the mice differ in, measured or not:
#   $P_0(p \le \alpha) \le \alpha$, the probability taken over the random assignments.
#   Fisher (1935, p. 24): "the simple precaution of randomisation will suffice to guarantee the validity of the test of significance".
#   When the labels were assigned at random, the shuffle test is also called a **randomization test**.
# - One random assignment balances the groups only on average, and the test allows for the rest.
#   The ARRIVE guidelines for animal research go a step further:
#   randomize within blocks, for example two drug and two control mice in every cage, chosen by chance,
#   and then shuffle within cages (Percie du Sert et al., 2020, Box 4).
#   That design, blocking, is beyond this notebook.
# - **Haphazard is not random.** "Selecting an animal 'at random' (i.e., haphazardly or arbitrarily) from a cage
#   is not statistically random, as the process involves human judgement" (Percie du Sert et al., 2020, item 4a).
#   Whichever mouse comes to hand first is exactly the first-caught allocation.
# - **Random assignment is not random sampling.** Notebook 1 sampled at random from a population.
#   Here chance assigns treatments to the mice you have,
#   which supports "the drug did it, in these mice" (Ernst, 2004);
#   it does not by itself make these mice stand for all mice.

# %% [markdown]
# ## Randomized, but who scores the mice?
#
# The same lab's next experiment is notebook 7's fear-memory test,
# with freezing scored by eye from video, as a percentage of time.
# The groups are randomized properly, and the drug does nothing:
# both groups freeze 50% of the time on average, with a standard deviation of 17 points.
# But the person scoring the videos knows which mice got the drug, and expects them to freeze less.
#
# **The simulation shades each drug-treated mouse's score 4 points lower, without anyone meaning to.
# The size is borrowed from human trials: assessors who knew the treatment rated outcomes
# 0.23 standard deviations better than blinded assessors of the same patients (Hr&oacute;bjartsson et al., 2013),
# and 0.23 x 17 is about 4.**
#
# **Predict first:** the groups were randomized. How often will the test call this useless drug significant?
# Choose your answer in the menu on the right side of the next cell, then run that cell.

# %%
# Choose your prediction in the menu on the right of this cell, then run the cell.
# The menu rewrites the line below; do not edit it by hand.
prediction_scorer = "choose"  # @param ["choose", "about 5%: the groups were randomized", "more than 5%"]

# %%
assert prediction_scorer != "choose", "Choose your prediction in the menu on the right of the cell above, then run that cell."

n = 20  # mice per group, randomized
for scorer in ["blind", "knows the groups"]:
    p_values = []
    for i in range(1000):
        control = rng.normal(50, 17, size=n)  # % of time freezing; the drug does nothing
        treated = rng.normal(50, 17, size=n)
        if scorer == "knows the groups":
            treated = treated - 4  # scores shaded toward what the scorer expects
        p_values.append(shuffle_test(control, treated))
    print(scorer, (np.array(p_values) <= 0.05).mean())

# %% [markdown]
# <details>
# <summary>Answer</summary>
#
# Blind: about 5%. Knowing the groups: about 11%, twice as often, and about 18% if you rerun with `n = 40`.
# Randomization keeps hidden differences out of who gets the drug;
# it cannot keep them out of how the outcome is measured.
# That is the job of **blinding**: the people who give the treatment, measure the outcome, and analyse the data
# do not know which group a mouse is in, until the analysis is done.
# A third party holds the code.
# Across the life sciences, studies done without blinding report larger effects and more significant p-values
# (Holman et al., 2015).
# Fisher's guarantee for randomization came with this exception spelled out:
# it holds "apart ... from the avoidable error of the experimenter himself introducing ... other differences in treatment"
# (Fisher, 1935, p. 24).
#
# </details>

# %% [markdown]
# ## Write the design down for approval
#
# An animal experiment needs approval before it starts:
# at Champalimaud, through the ORBEA and the DGAV, following the Vivarium's standard operating procedures
# (see Ana Machado's slides).
# The approval asks, among much else, how the animals will be allocated, who will be blinded, and why this many animals.
# Two cells do most of that writing for you.
#
# **A randomisation sheet.** `["A"] * 6 + ["B"] * 6` is a list of six A's and six B's;
# `rng.permutation` shuffles it, one letter per mouse.
# A third party decides, and keeps to themselves, which letter is the drug,
# and prepares the syringes labelled by mouse number only.
# Everyone else sees only the letters until the analysis is done.

# %%
codes = rng.permutation(["A"] * 6 + ["B"] * 6)
for i in range(12):
    print("mouse", i + 1, codes[i])

# %% [markdown]
# **The design paragraph.**
# The form on the right of the next cell is filled in for the temperature experiment above.
# Run it, then run the cell after it: it prints the design as a paragraph.
# Then change the fields to describe an experiment of your own, rerun both cells, and copy the paragraph.
# Take the number of animals from notebook 7.
# The order and wording follow Ana Machado's slide "Reporting a design experiment"
# (Machado, 2024), which also shows a full worked example.

# %%
# Fill in the form on the right; each line below is one field.
question = "whether drug X lowers body temperature"  # @param {type:"string"}
animals = "group-housed adult C57BL/6J mice"  # @param {type:"string"}
treatment = "drug X, 10 mg/kg, injected intraperitoneally"  # @param {type:"string"}
control = "saline, the vehicle, injected the same way"  # @param {type:"string"}
outcome = "rectal temperature (C), one hour after the injection"  # @param {type:"string"}
unit = "mouse"  # @param ["mouse", "cage", "litter", "part of the animal"]
third_party = "a lab member who does not handle or measure the animals"  # @param {type:"string"}
difference = 1.0  # @param {type:"number"}
sd = 0.8  # @param {type:"number"}
power = 0.8  # @param {type:"number"}
n_per_group = 12  # @param {type:"integer"}

# %%
print(f"We will test {question} in {animals}, comparing {treatment} with {control}.")
print(f"The experimental unit is the {unit}: each {unit} can be allocated to a treatment group independently of the others.")
print(f"The {2 * n_per_group} units are allocated at random to two groups of {n_per_group}, using a computer-generated randomisation sheet.")
print(f"The allocation is held by {third_party}, who prepares the doses labelled by animal number only, "
      "so that the person giving them does not know which animal receives which treatment.")
print(f"The outcome measure is {outcome}. It is measured blind: the allocation is revealed only after all measurements are done.")
print(f"There is one independent variable of interest, the treatment, with two categories: {control}, and {treatment}.")
print("The analysis is also carried out blind, on groups coded A and B: "
      "a two-sided shuffle (randomization) test of the difference in group means, at a significance level of 0.05.")
print(f"Sample size: a difference of {difference} in {outcome} is the smallest considered biologically important, "
      f"and earlier experiments give a standard deviation of {sd}. "
      f"With a significance level of 0.05 and a power of {power}, simulating the planned experiment gives {n_per_group} animals per group.")

# %% [markdown]
# Before you submit a real design, check it against the ARRIVE Essential 10
# (https://arriveguidelines.org/arrive-guidelines), and draw it with the NC3Rs Experimental Design Assistant
# (https://eda.nc3rs.org.uk), which can also generate the randomisation sheet.

# %% [markdown]
# ## You can now...
#
# assign treatments at random, blind the people who treat and measure,
# and write the design so that an approval committee can check it.
#
# Shortcuts in allocation are old.
# In 1930, a study of milk at school in Lanarkshire gave milk to 10000 of 20000 schoolchildren.
# Teachers then swapped some children "in order to obtain a more level selection".
# After the swaps, the children without milk were heavier and taller than the milk children before the study began,
# probably because the teachers, without meaning to, gave the milk to the poorer children (Student, 1931).
# Before trusting any comparison, ask the question Cobb (2007) asks students to ask of every study:
# "Where was the randomization, and what inferences does it support?"
#
# ## Why randomize?
#
# Let chance decide who gets the drug, so that nothing else can.

# %% [markdown]
# ## Stretch (optional)
#
# > **Stretch (optional): the drug in the drinking water.**
# > When the drug goes into a cage's water bottle, every mouse in the cage gets the same treatment.
# > Then the cage, not the mouse, is the experimental unit: cages are what you randomize, and cages are what you shuffle
# > (Lazic et al., 2018).
# > Cages differ from one another, too.
# > In a new cell, simulate 4 cages per group with 5 mice per cage and a drug that does nothing:
# > each cage's typical temperature is 36.5 plus `rng.normal(0, 0.4)`, and its mice vary around it with a standard deviation of 0.8.
# > Randomize the cages, then compare two tests over 1000 experiments:
# > shuffling the 40 mice, and shuffling the 8 cage averages.
#
# <details>
# <summary>Answer</summary>
#
# ```python
# p_mice = []
# p_cages = []
# for i in range(1000):
#     cage_typical = 36.5 + rng.normal(0, 0.4, size=8)                    # 8 cages; the drug does nothing
#     temps = np.repeat(cage_typical, 5) + rng.normal(0, 0.8, size=40)    # 5 mice per cage
#     cage_group = rng.permutation(["drug"] * 4 + ["control"] * 4)        # cages randomized
#     mouse_group = np.repeat(cage_group, 5)
#     p_mice.append(shuffle_test(temps[mouse_group == "control"], temps[mouse_group == "drug"]))
#     cage_avg = temps.reshape(8, 5).mean(axis=1)                         # one average per cage
#     p_cages.append(shuffle_test(cage_avg[cage_group == "control"], cage_avg[cage_group == "drug"]))
# print("shuffle mice:", (np.array(p_mice) <= 0.05).mean())
# print("shuffle cages:", (np.array(p_cages) <= 0.05).mean())
# ```
#
# Shuffling mice calls the useless drug significant about 15% of the time;
# shuffling cage averages, at most 5%.
# Shuffling mice pretends that each mouse was randomized on its own, as notebook 6's readings pretended to be mice.
# One more catch: with 4 cages per group there are only 70 ways to split the 8 cages,
# so the smallest two-sided p-value is 2/70, about 0.03.
# With 3 cages per group (20 splits) it is 0.1, and the test can never reach 0.05, however large the effect:
# plan enough cages, not just enough mice.
#
# </details>

# %% [markdown]
# ## References
#
# Cobb, G. W. (2007). The introductory statistics course: A Ptolemaic curriculum?
# *Technology Innovations in Statistics Education, 1*(1). https://doi.org/10.5070/t511000028
#
# Ernst, M. D. (2004). Permutation methods: A basis for exact inference.
# *Statistical Science, 19*(4), 676-685. https://doi.org/10.1214/088342304000000396
#
# Fisher, R. A. (1935). *The design of experiments*. Oliver and Boyd.
#
# Holman, L., Head, M. L., Lanfear, R., & Jennions, M. D. (2015).
# Evidence of experimental bias in the life sciences: Why we need blind data recording.
# *PLOS Biology, 13*(7), e1002190. https://doi.org/10.1371/journal.pbio.1002190
#
# Hr&oacute;bjartsson, A., Thomsen, A. S. S., Emanuelsson, F., Tendal, B., Hilden, J., Boutron, I., Ravaud, P., & Brorson, S. (2013).
# Observer bias in randomized clinical trials with measurement scale outcomes:
# A systematic review of trials with both blinded and nonblinded assessors.
# *Canadian Medical Association Journal, 185*(4), E201-E211. https://doi.org/10.1503/cmaj.120744
#
# Lazic, S. E., Clarke-Williams, C. J., & Munaf&ograve;, M. R. (2018).
# What exactly is 'N' in cell culture and animal experiments?
# *PLOS Biology, 16*(4), e2005282. https://doi.org/10.1371/journal.pbio.2005282
#
# Machado, A. (2024). *Steps in designing a randomised controlled animal experiment* [Lecture slides].
# Champalimaud Foundation.
#
# Percie du Sert, N., Ahluwalia, A., Alam, S., Avey, M. T., Baker, M., Browne, W. J., Clark, A., Cuthill, I. C., Dirnagl, U., Emerson, M., Garner, P., Holgate, S. T., Howells, D. W., Hurst, V., Karp, N. A., Lazic, S. E., Lidster, K., MacCallum, C. J., Macleod, M., ... W&uuml;rbel, H. (2020).
# Reporting animal research: Explanation and elaboration for the ARRIVE guidelines 2.0.
# *PLOS Biology, 18*(7), e3000411. https://doi.org/10.1371/journal.pbio.3000411
#
# Student. (1931). The Lanarkshire milk experiment.
# *Biometrika, 23*(3/4), 398-406. https://doi.org/10.2307/2332424
#
# Takao, K., Shoji, H., Hattori, S., & Miyakawa, T. (2016).
# Cohort removal induces changes in body temperature, pain sensitivity, and anxiety-like behavior.
# *Frontiers in Behavioral Neuroscience, 10*, 99. https://doi.org/10.3389/fnbeh.2016.00099
