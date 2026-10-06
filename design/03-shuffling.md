# Notebook 3: shuffling - the null hypothesis of independence - design

Status: approved 2026-10-05 with every decision at its recommended default
("repeating once is fine" for decision 5).
Implemented in `notebooks/03_shuffling.py`, paired with `.ipynb` for Colab.
Scope settled with Memming on 2026-10-05:
two groups with shuffled labels (not a scatter), carried through the p-value, two plots,
and the link between independence, exchangeability, and exactness cited rigorously.
Found while implementing (see Visualization): the shuffle histograms are lumpy, not bells,
and the answers explain why.
Built from a prior-art survey (see `AGENTS.md`, "Starting a new notebook"):
`old_ref/` and its books, interactive tools, Python notebooks, courses, GitHub,
misconception research, the theory of permutation tests,
and open data from cancer immunology and neuroscience.

## Where it sits

Day 2 morning, after the paper worksheet `worksheets/coin_test.tex`
and before "Implement your own hypothesis test".
On the worksheet, students wrote the recipe of a test
(null hypothesis, test statistic, its sampling distribution under the null, decision rule)
and met the p-value at the board.
It serves the `README.md` objective
"Use shuffling to generate sampling distributions under independence",
under the `README.md` heading "Shuffling and Permutation, how to break dependence".

What it adds to the worksheet:
the coin's null hypothesis fixed the probability of every result, so the binomial table was the sampling distribution.
"The antibody does nothing" fixes no distribution for tumor volume.
It fixes only that every way of labeling the mice is equally likely,
and shuffling turns that into a sampling distribution.

## Final observation

"Shuffled labels show the differences a useless drug would produce,
so a real difference that few shuffles reach is evidence that the drug did something."

## Python practice

Shuffling an array with `rng.permutation` and dealing it into two groups with slices (`[:5]`, `[5:]`),
repeated in a `for` loop that collects one difference per shuffle.
Students write the p-value line themselves (step 4) with notebook 1's compare-then-average move.
The loop is the general pattern the next activity needs:
simulate under the null, compute the statistic, record it, repeat.

## Data

Sipe et al. 2022, eLife 11:e79143, https://doi.org/10.7554/eLife.79143, Figure 5B:
tumor volume at endpoint (mm^3) of E0771 breast tumors in female C57BL/6J mice,
injected every third day with anti-PD-L1 or an IgG2b isotype control antibody, 5 mice per group.
Source data https://zenodo.org/records/6858951 (CC0), sheet "Figure 5B", read 2026-10-05.

| Mice | Control (IgG2b) | anti-PD-L1 | Means | Difference |
|---|---|---|---|---|
| Lean (LFD-Sham) | 542.8, 83.0, 555.3, 482.8, 556.6 | 0.0625, 70.2, 0.0625, 256.5, 28.5 | 444.1 vs 71.1 | 373.0 |
| Obese (HFD-Sham) | 4540.1, 2019.2, 2126.9, 1928.4, 1759.0 | 674.6, 2374.7, 1679.2, 3976.6, 2193.5 | 2474.7 vs 2179.7 | 295.0 |

The paper computes volume = width^2 x length / 2 from caliper measurements,
so 0.0625 mm^3 is a tumor 0.5 mm across; it does not say this is a detection floor.

**The notebook uses whole mm^3**: lean 543, 83, 555, 483, 557 | 0, 70, 0, 257, 29 (difference 373.0);
obese 4540, 2019, 2127, 1928, 1759 | 675, 2375, 1679, 3977, 2194 (difference 294.6).
The reason is floating point, found by the independent review on 2026-10-06:
with decimals, a shuffle that reproduces the real split sums the same five values in another order,
the mean can land a hair below `observed`, and `>=` misses it.
Over 200000 shuffles the decimal version gave p = 0.0055 one-sided against the exact 0.0079;
the whole-number version gave 0.0082.
Sums of whole numbers are exact in any order, so ties are counted.
A collapsed note in the notebook explains this and gives `diffs >= observed - 1e-9` for decimal data,
which the next activity ("Implement your own hypothesis test") will need.
Every exact count below is the same for the whole-number values.
Computed 2026-10-05 from the source values:

| Mice | Exact, all C(10,5) = 252 splits, one-sided / two-sided | 10000 shuffles, seed 20261005, one-sided / two-sided | SD of shuffled differences |
|---|---|---|---|
| Lean | 2/252 = 0.0079 / 4/252 = 0.016 | 0.0086 / 0.0161 | 158 |
| Obese | 86/252 = 0.34 / 172/252 = 0.68 | 0.352 / 0.683 | 712 |

The two differences are of similar size, and their verdicts are opposite:
the obese tumors vary so much more that shuffles alone produce 295 routinely.
The second lean labeling at or beyond 373 swaps the 257 mm^3 anti-PD-L1 tumor with the 83 mm^3 control tumor (442.6).
Shuffled lean differences span -442.6 to 442.6 (central 95%: -281 to 281); obese, -1430.6 to 1430.6.

Allocation: the paper states that diets were randomized
and that "group allocation was done to ensure equal distribution of starting body weight between groups";
it does not say how mice were allocated to the two antibodies.
So the notebook never claims random assignment.
It justifies shuffling by exchangeability under the null hypothesis
(Ernst 2004's population model, below): if the antibody does nothing,
and the drug went to mice picked without regard to their tumors,
which five of the ten mice carry the drug label does not matter.
The notebook states that allocation assumption in step 2 and again at naming
(added after the independent review: independence of volume and label alone
does not answer step 1's question if allocation could have followed the tumors).

## Rigor: what the notebook states, and the sources

1. **Independence makes the shuffles the exact null distribution.**
   If tumor volume does not depend on the antibody,
   and the drug went to mice picked without regard to their tumors,
   the ten values are exchangeable: their joint distribution is unchanged by reordering them.
   Then, given the ten values observed, every one of the 252 labelings is equally likely,
   so the shuffled differences are the sampling distribution of the difference under the null,
   exactly, conditional on the values,
   and a test that rejects when p <= alpha wrongly rejects a true null with probability at most alpha.
   Lehmann and Romano, *Testing Statistical Hypotheses*, 3rd ed. (2005),
   Sec. 15.2.1, Def. 15.2.1 and Thms 15.2.1-15.2.2, pp. 632-636,
   with Ex. 15.2.2 (two samples) and Ex. 15.2.3 (independence), https://doi.org/10.1007/0-387-27605-X_15;
   Ernst 2004, Sec. 4.1, pp. 680-681, https://doi.org/10.1214/088342304000000396.
   In a randomized experiment the random assignment alone justifies the same count,
   with no sampling from a population (Ernst 2004, Sec. 3; Lehmann and Romano Sec. 5.12, pp. 187-188).
2. **Random shuffles stay valid when the real labeling is counted as one of them**:
   p = (1 + b) / (1 + m), with b of m shuffles at least as extreme, is a valid p-value for any m, and never 0.
   Ernst 2004, Sec. 4.2, p. 682;
   Lehmann and Romano, Eqs. (15.7)-(15.8), p. 636;
   Hemerik and Goeman 2018, TEST 27:811-825, Thm 2, https://doi.org/10.1007/s11749-017-0571-1;
   Phipson and Smyth 2010, Stat Appl Genet Mol Biol 9:39, Secs. 4-6, https://doi.org/10.2202/1544-6115.1585.
   "At most alpha" is the guarantee; exactly alpha needs no ties, shuffles without repeats,
   and alpha a multiple of 1/(m + 1) (Hemerik and Goeman, Prop. 2).
3. **The null hypothesis is "the label does not matter at all", not "the means are equal".**
   If two groups differ only in spread, the shuffle test of a difference in means
   is not exact for "equal means", and with unequal group sizes not even approximately valid in large samples.
   Romano 1990, JASA 85:686-692, https://doi.org/10.1080/01621459.1990.10474928
   (read as the 1989 Stanford report, https://purl.stanford.edu/vn959zz4291, Thm 3.1 and Cor. 3.1);
   Chung and Romano 2013, Ann. Statist. 41:484-507, Sec. 1 and Thm 2.2, https://doi.org/10.1214/13-AOS1090;
   Lehmann and Romano, Thm 15.2.5, pp. 642-643.

The notebook's "For deeper mathematics" line cites Ernst 2004, Sections 3-4:
free, short, it proves exactness by counting, separates random assignment from random sampling,
and gives the +1 formula.
Not Wasserman Sec. 10.5, which matches notebook 2's citation style
but has no proof and counts with a strict ">" and no +1 (see Rejected).

## Step ladder

About 15 minutes.
At most one new thing per step.
A setup cell creates `rng = np.random.default_rng(20261005)` once;
`runs = 10000` is set where it is first used (step 3) and is never a knob, as in notebook 2.

1. **Ten mice, two antibodies.**
   The lean mice from Sipe et al. 2022, as one array:
   `volumes = np.array([...])`, the five control mice first, then the five anti-PD-L1 mice.
   `volumes[:5]` and `volumes[5:]` printed raw, then their means,
   then `observed = volumes[:5].mean() - volumes[5:].mean()`: 373 mm^3.
   Prose asks: tumors differ from mouse to mouse;
   could the drug group simply have drawn the small ones?
   New: `np.array([...])`; `[5:]` beside the familiar `[:5]` (notebook 1).
2. **If the drug did nothing, the labels would be arbitrary.**
   If anti-PD-L1 did nothing, and the drug went to mice picked without regard to their tumors,
   each tumor would have grown to the same size whichever antibody its mouse got,
   so any five of the ten mice could have carried the drug label:
   if the labels do not matter, the real labeling should look like any shuffled one.
   (Not VanderPlas's "switching them shouldn't change the result":
   the next cell shows that a shuffle does change the difference.)
   `rng.permutation(volumes)` printed raw: the same ten numbers in a new order.
   Deal the first five as "control", the rest as "anti-PD-L1", and print the difference.
   Run the cell again a few times: did any shuffle reach 373?
   Collapsed answer: rarely; most shuffled differences fall within a few hundred mm^3 of 0.
   New: `rng.permutation`. Active: rerun.
3. **Predict, then shuffle 10000 times.**
   The heading states a claim that does not give the prediction away
   ("Ten thousand shuffles show what a useless drug would produce").
   Form dropdown with the `assert` gate:
   "Where will the shuffled differences center?" (around 0 / around 373 / around 187).
   A `for` loop collects `runs` shuffled differences (`diffs.append(...)`, as in notebook 1),
   then `diffs = np.array(diffs)`.
   Histogram of `diffs`, one vertical line at `observed`,
   x-axis "difference after shuffling, control minus anti-PD-L1 (mm^3)".
   Prose asks: what is one value in this histogram?
   Collapsed answers: centered on 0, because each shuffled group is a random five of the same ten mice;
   one value is one way the experiment could have come out if the drug did nothing.
   New: the shuffle loop and `plt.axvline` (notebook 1 used `plt.axhline`). Active: predict.
4. **How often does a shuffle do as well? The p-value.**
   The direction is stated before counting: the drug is meant to shrink tumors,
   so count shuffles whose difference is at least as large as the real one.
   Students fill `p_value = ...` with `(diffs >= observed).mean()`.
   Collapsed answer: about 0.008, give or take a few thousandths.
   The shuffled differences play the role the binomial table played on the worksheet,
   and this fraction is the p-value from the board.
   Counting both directions, `(np.abs(diffs) >= observed).mean()`, gives about 0.016, twice as large.
   Collapsed "Why 252? (optional)":
   there are C(10, 5) = 252 ways to choose which five mice carry the drug label
   (the worksheet's "n choose k"), all equally likely if the drug does nothing;
   only 2 of them give a difference of 373 or more, the real labeling
   and the one swapping the 257 and 83 mm^3 tumors: 2/252 = 0.008.
   Collapsed "Why whole numbers? (optional)": the floating-point reason (see Data),
   with `diffs >= observed - 1e-9` for decimal data.
   Collapsed "Why some add 1 (optional)": claim 2 above, with "valid" defined
   (rejects a true null at most 5% of the time at the 0.05 level);
   if no shuffle reaches the observed difference, the rule gives 1/10001, never 0.
   New: none beyond the p-value as a count of shuffles. Active: fill one line.
5. **Name it.**
   The student says in their own words what the shuffles showed (collapsed answer).
   Then the names:
   the **null hypothesis of independence** (tumor volume does not depend on the antibody),
   under which the ten values are **exchangeable** and every labeling is equally likely (claim 1);
   the **permutation test**, also called a shuffle or randomization test:
   the worksheet's recipe with shuffling in its step 3;
   the formula, p = (number of shuffles with a difference at least as large as the observed one) / (number of shuffles).
   One sentence on claim 3: the test asks whether the label matters at all, not only whether the means differ.
   **For deeper mathematics:** Ernst 2004, Sections 3-4.
6. **Worked transfer: the same drug in obese mice.**
   An ungated cell prints the obese volumes and their difference first, as step 1 did,
   so the prediction can use the spread (added after the review).
   Their difference is 295 mm^3, almost as large as the lean mice's 373.
   Form dropdown: "How often will a shuffle reach 295?" (rarely, like the lean mice / often / never).
   One cell repeats steps 3-4 on the obese values: the loop, the histogram, the p-value.
   Collapsed answer: often, about 1 shuffle in 3 (p about 0.34), with the three humps explained.
   The obese tumors vary far more (control 1759 to 4540 mm^3),
   so shuffling alone routinely produces differences of 295:
   the size of a difference does not say whether chance could produce it.
   And a large p-value is not evidence that the drug fails in obese mice:
   five mice per group cannot tell a modest effect from none.
   New: none. Active: predict.
7. **You can now ...**
   test whether a difference between two groups could come from chance alone, with no formula:
   shuffle, recompute, count.
   `scipy.stats.permutation_test` does the same, for the record; it counts both directions by default.
   The caveat: shuffle the units that are exchangeable under the null hypothesis,
   the mice, not cells from one mouse or time points of one recording,
   whose values are not independent (notebook 2: N counts mice, not trials).
   Last, the concept in one plain sentence:
   "If the labels do not matter, shuffling them shows what chance alone would produce."

**Stretch (optional):**
- **CD8+ T cells, lean vs obese.**
  Sipe et al. 2022, Figure 4B (same CC0 file): tumor CD8+ T cells as % of live cells,
  given in the notebook as whole cells per 10000 live cells, so sums are exact (see Data):
  lean 104, 74, 31, 66, 38, 43, 22, 49 (8 mice);
  obese 28, 38, 28, 20, 20, 16, 22 (7 mice).
  Diets were randomized, as the paper states, but diet-resistant mice were excluded from the obese group.
  Unequal group sizes: the student changes the split from 5 to 8.
  Exact over all 6435 splits: 20/6435 = 0.0031 one-sided, 56/6435 = 0.0087 two-sided.
- **Shuffle one neuron's trials: noise correlation.**
  Two neurons' spike counts on 200 trials of one stimulus,
  **simulated for teaching purposes** with a shared input (`rng.poisson`),
  correlation about 0.2, in the range Cohen and Kohn 2011 report (0.01-0.26).
  Shuffling one neuron's trial order breaks the shared trial-to-trial variation
  and leaves each neuron's counts unchanged (Kafashan et al. 2021);
  the correlation of shuffled pairs gives the null distribution.
  Printed numbers only, no plot.
  New: `np.corrcoef`, `rng.poisson`.
  True correlation 1/6. Over 300 simulated sessions of 200 trials,
  r fell between 0.04 and 0.28 (5th to 95th percentile) and p < 0.05 in 74%,
  so the answer reports a range ("about 3 of 4 sessions").

Budget: 7 steps, 4 active moments (2, 3, 4, 6), two plots (steps 3 and 6).

Python constructs met, in order:
`np.array([...])`, `[:5]` and `[5:]`, `.mean()`, `round(x, 1)` for printing, `rng.permutation`,
a `for` loop with `.append` (notebook 1), `plt.hist`, `plt.axvline`, `>=` then `.mean()`.
The setup cell also sets `np.set_printoptions(suppress=True)`, commented:
without it, 0.1 beside 556.6 prints the whole array in scientific notation.
Assumed known: `for` loops, lists, `print`, f-strings, form dropdowns and the `assert` gate (notebooks 1-2).
Deliberately absent: `rng.shuffle` (works in place and returns `None`, so its raw output misleads),
`np.tile` and `rng.permuted` (decision 4), `itertools.combinations` (the 252 is stated, not enumerated),
pandas, and any t statistic (Day 3).

## Visualization

Printed numbers everywhere except two histograms of shuffled differences,
lean (step 3) and obese (step 6), each with one vertical line at the observed difference
and the x-axis "difference after shuffling, control minus anti-PD-L1 (mm^3)".
Each keeps its own x-scale; the obese axis spans about three times the lean one,
so the markdown says to compare where the line falls, not the widths.
No plot of the ten raw values: printed, they are the object (step 1).

Both histograms are lumpy, not the bell students saw in notebook 2,
and the answers say so instead of hiding it.
Lean: four tumors are far larger than the rest (483 to 557 mm^3),
so the humps follow how many of those four a shuffle deals to each group, and where the 257 one goes
(checked by grouping all 252 splits).
Obese: three humps; shuffles that put the two largest tumors (4540 and 3977) in the same group
give differences of 397 to 1430 either way, and shuffles that split them stay under 650,
where 295 falls.
The point it makes: a permutation test needs no bell, only a count.

## Adopted

| Source | What we took |
|---|---|
| Simon, *Resampling: The New Statistics*, Ex. 18-2 and 18-5, pp. 278-288 (`old_ref/books/02_resampling_book/`); open edition, Simon and Brett, *Resampling with*, ch. 24, https://resampling-stats.github.io/latest-python/testing_measured.html | Pool the values and deal them into groups of the original sizes, without replacement; a few shuffles shown before many (steps 2, 3) |
| Data 8 ch. 12.1, https://inferentialthinking.com/chapters/12/1/ab-testing/index.html | One shuffled dataset shown beside the original before any histogram; group sizes kept fixed; the null as "the labels don't matter" (step 2) |
| ModernDive ch. 9, https://moderndive.com/9-hypothesis-testing.html | Original and shuffled labels side by side; the terms named only after the phenomenon (steps 2, 5) |
| VanderPlas, *Statistics for Hackers*, https://speakerdeck.com/jakevdp/statistics-for-hackers | "If the labels really don't matter, switching them shouldn't change the result" (step 2); a case whose observed value lands in the bulk, as a prediction (step 6) |
| Downey, *Think Stats* ch. 9, https://allendowney.github.io/ThinkStats/chap09.html | `(diffs >= observed).mean()` as the p-value (step 4) |
| Downey, "There is only one test", http://allendowney.blogspot.com/2011/05/there-is-only-one-test.html | The shuffle mapped onto the one recipe (statistic, null model, simulate, count) at naming (step 5) |
| Broman, permutation test notes, https://kbroman.org/AdvData/21_permtest_notes.pdf | "Exchangeable" glossed as "the labels don't matter" (step 5); the number of shuffles fixed, not a knob |
| PH525, Harvard, https://genomicsclass.github.io/book/pages/permutation_tests.html | The +1 rule with Phipson and Smyth, in a collapsed note (step 4) |
| Online Stat Book, https://onlinestatbook.com/2/distribution_free_tests/randomization_two.html | Exact enumeration as what the shuffles approximate, stated as a count, not computed (step 4, "Why 252?") |
| Kass, Eden and Brown, *Analysis of Neural Data*, Sec. 11.2.1, pp. 297-301; pp. 245, 320 (`old_ref/books/`) | Counting with ">="; the floor of 1/(number of shuffles); shuffle only independent units (steps 4, 7) |
| Case and Jacobbe 2018, SERJ 17(2), https://doi.org/10.52041/serj.v17i2.156 | Keep data, one shuffle, and the distribution apart: one shuffle printed first, "what is one value in this histogram?", predict the center (steps 2, 3) |
| Budgett, Pfannkuch, Regan and Wild 2013, TISE 7(2), https://doi.org/10.5070/T572013889 | Data, then one shuffle, then the distribution, top to bottom; the observed value marked on the distribution (steps 1-3) |
| Holcomb, Chance, Rossman, Tietjen and Cobb 2010, ICOTS8, https://iase-web.org/documents/papers/icots8/ICOTS8_8D1_HOLCOMB.pdf | A clearly significant first example; the unsurprising one second (lean before obese) |
| Gould, Davis, Patel and Esfandiari 2010, ICOTS8, https://iase-web.org/documents/papers/icots8/ICOTS8_C208_GOULD.pdf | Axis labelled "difference after shuffling", so the null distribution is not read as the data (steps 3, 6) |
| Lane-Getaz 2013, SERJ 12(1), https://iase-web.org/documents/SERJ/SERJ12(1)_LaneGetaz.pdf | The direction stated in prose before the count (step 4) |
| Chance, Tintle et al. 2022, SERJ 21(3), https://doi.org/10.52041/serj.v21i3.6; Lytsy, Hartman and Pingel 2022, https://doi.org/10.48101/ujms.v127.8760 | "A large p-value is evidence for the null" grows after instruction, and medical PhD students hold it too: the obese answer says it explicitly (step 6) |
| Sipe et al. 2022, https://doi.org/10.7554/eLife.79143, data https://zenodo.org/records/6858951 (CC0) | Core data (Fig. 5B) and the CD8 stretch (Fig. 4B) |
| Harris 2020, https://doi.org/10.1101/2020.11.29.402719; Elber-Dorozko and Loewenstein 2018, https://doi.org/10.7554/eLife.34248 | Shuffling time points of drifting signals gives false positives: the caveat in step 7 |
| Kafashan et al. 2021, https://doi.org/10.1038/s41467-020-20722-y; Cohen and Kohn 2011, https://doi.org/10.1038/nn.2842 | Trial shuffling within one stimulus breaks noise correlation; typical size (stretch) |
| Ernst 2004; Lehmann and Romano 2005; Hemerik and Goeman 2018; Phipson and Smyth 2010; Romano 1990; Chung and Romano 2013 | The three claims in "Rigor" and the "For deeper mathematics" line |

## Rejected

| Source | What | Why |
|---|---|---|
| Simon Ex. 15-5, 15-7, 18-1, 18-3, 18-4; *Resampling with* ch. 21, 24 | Two-group tests by resampling with replacement, even after random assignment | A second resampling scheme in one notebook; for the mice it also changes the answer |
| Simon p. 221 | The cancer pill "obviously a one-tail test" | The direction comes from belief instead of a choice fixed before the data, against the worksheet |
| Simon p. 359 | The p-value read as the probability of no relationship | Contradicts the worksheet key ("not the probability that the dealer is honest") |
| Simon p. 373; Data 8 ch. 12.1 | "0 of 1000" reported as p = 0, and a printed 0.0 | A p-value is never 0 (claim 2) |
| Wasserman, *All of Statistics* Sec. 10.5, pp. 161-164 (`old_ref/books/`) | Counting with a strict ">" and no +1 | Its toy example gets 4/6 where ">=" gives 1; Ex. 10.20 moves from 0.119 to 0.048 on ties |
| Kass Sec. 11.2.1 | A shuffled t statistic | Needs a pooled-SD formula before naming; t-tests are Day 3 |
| Kass p. 300 | Bootstrap step comparing \|t\| with a negative t_obs | Bug: gives p = 1 |
| Last year's Day 4 activity 1, Ex. 3 (`old_ref/Day4 activity/`) | A drug test on "100 cells from both groups" | Pseudoreplication, contradicting its own experimental-unit lesson |
| Last year's Day 4 activity 3, `plot_power_anatomy` | One tail shaded and labelled alpha; global `np.random.seed(42)` | The shaded area is alpha/2; global seed (out of scope here, recorded for the power notebook) |
| StatKey, https://www.lock5stat.com/StatKey/randomization_1_quant_1_cat/randomization_1_quant_1_cat.html; Rossman/Chance, https://www.rossmanchance.com/applets/2021/anovashuffle/AnovaShuffle.htm; Art of Stat, https://istats.shinyapps.io/PermDist_2samples/ | Dataset menus, statistic dropdowns, tail checkboxes, several generate buttons | A dashboard |
| StatKey | Tail cutoff at the 2.5% quantile | The count must start from the observed value |
| Rossman/Chance; Art of Stat; Broman | A t density or t-test beside the shuffles | One phenomenon; Day 3 |
| Roach, https://github.com/croach/statistics-for-hackers | pandas, and `np.random.shuffle` on the global generator | One seeded `rng`; in-place shuffling returns `None` |
| Kramer and Eden ch. 2, https://github.com/Mark-Kramer/Case-Studies-Python | Resampling with replacement called a permutation test; `seed(123)` inside the analysis cell | Mislabelled scheme; reruns would be identical |
| Kramer and Eden STN neuron (`10_spikes-1.mat`) | 25 vs 25 trials, left vs right | The groups do not overlap; p is essentially 0, too easy to teach the null |
| Data 8 ch. 12.1 (1174 babies); StatKey (n = 1000 per group) | Large data as the first system | Smallest system first; ten values fit on screen |
| Oxford StatsCourseBook, https://jillxoreilly.github.io/StatsCourseBook_2024/Chapter4_PermutationTest/MT_wk5_permutation_unpaired.html | `scipy.stats.permutation_test` on the core path; four shuffle plots | Code that is the concept stays visible; plot budget. Scipy is named under "you can now" |
| Online Stat Book | Enumerating all 70 splits in code | Needs `itertools.combinations`; the count is stated instead |
| Budgett et al. 2013 | Animated dots; a 10% guideline | Students made the guideline a rigid cutoff and read the tail as effect size; the worksheet already fixed alpha |
| Wilber, https://www.jwilber.me/permutationtest/ | Scroll-driven animation | Not editable; one new thing per step |
| Sipe et al. 2022, Fig. 6D | Ido1 expression vs tumor volume, r = -0.55 | Ido1 was selected for correlating with tumor volume, so its p is inflated; two diets pooled |
| Rossman/Chance default data (sleep deprivation, Stickgold 2000) | Neuroscience transfer | Not checked against its source; the obese mice and the CD8 stretch cover the transfer |
| Notebook 2's one-row-per-run, `rng.permuted(np.tile(volumes, (runs, 1)), axis=1)` | Shuffling in one call | `np.tile`, `permuted`, and 2-D slicing would be three new constructs in one step (decision 4) |

## Deferred to later notebooks

- Shuffling one column of a scatter as the core picture of breaking dependence:
  Simon ch. 23 (cholostyramine dose vs cholesterol drop, `bootstrap::cholost`, BSD-3);
  *Resampling with* ch. 29, https://resampling-stats.github.io/latest-python/correlation_causation.html;
  Rossman/Chance regression shuffle, https://www.rossmanchance.com/applets/2021/regshuffle/regshuffle.htm;
  Oxford StatsCourseBook, https://sageboettcher.github.io/StatsCourseBook_2026/3.1_PermutationTest/3.1.9_permutation_correlation.html.
- Neuroscience nulls that shuffle differently:
  circular shifts for place cells (Talpir et al. 2025, https://doi.org/10.1016/j.isci.2025.112489),
  spike jitter (Amarasingham et al. 2012, https://doi.org/10.1152/jn.00633.2011),
  chance level for decoders (Combrisson and Jerbi 2015, https://doi.org/10.1016/j.jneumeth.2015.01.010).
- The maximum statistic over many tests (Kramer and Eden) and uniform p-values under the null (Kass p. 274):
  the multiple-testing activity, Day 2 afternoon.
- The studentized shuffle test for unequal spreads (Chung and Romano 2013): with the t-test, Day 3.
- Random assignment as the basis of causal claims, with potential outcomes (Data 8 ch. 12.2; Cobb 2007, https://doi.org/10.5070/T511000028).

## Decisions

Each has a recommended default; the alternative follows.

1. **Real data as the core system**, the lean mice of Sipe et al.,
   although `demo-design.md` says realism is not a goal:
   ten labelled numbers are already the smallest system that shows a shuffle, and these ten are real
   (not: invented 5 vs 5 values in the core, Sipe at the close).
2. **One-sided count in the fill line**, the direction stated in prose first; two-sided in the collapsed answer
   (not: two-sided in the fill line, which adds `np.abs` to the step).
3. **The plain fraction `(diffs >= observed).mean()` in the fill line**; the +1 in a collapsed note
   (not: `((diffs >= observed).sum() + 1) / (runs + 1)` in the core line,
   valid for any number of shuffles but no longer notebook 1's move;
   with 10000 shuffles the two differ by 0.0001 here).
4. **A `for` loop with `.append`**, notebook 1's idiom and the shape of the next activity
   (not: notebook 2's one-row-per-run; see Rejected).
   `design/02-averages.md` says shuffling would reuse that move; that sentence changes.
5. **The obese mice as the worked transfer**, one cell repeating the four-line loop, not a function
   (not: CD8 T cells as the transfer and the obese mice as a stretch).
6. **Exchangeability, not random assignment**, justifies the shuffle,
   because the paper does not say how mice were allocated to the antibodies.
7. **Keep the noise-correlation stretch**, the one neuroscience moment
   (not: defer it with the other scatter shuffles, keeping the notebook to one statistic).
8. **Outside the notebook, optional:** shuffle ten index cards carrying the lean volumes at the board before step 2.
   Hands-on before software helped in Hancock and Rummerfield 2020 (https://doi.org/10.1080/10691898.2020.1720551),
   and watching a physical shuffle before code helped in Zhang, Tucker and Stigler 2022 (https://doi.org/10.1016/j.compedu.2022.104545);
   Holcomb et al. 2010 found no difference. The first cell mentions it only if it is done.

## Changes elsewhere, made 2026-10-05

- `notebooks/02_averages.py` intro now points to the coin worksheet and this notebook,
  instead of "The next notebook looks more closely at the bell you will meet here".
- `design/02-averages.md`: "Where it sits" and "Python practice" updated to match.
- `README.md`: the Colab link under "Shuffling and Permutation, how to break dependence".

## Checks

2026-10-05, executed outside the repo as `colab.md` describes:
the notebook as shipped stops at the first prediction gate;
a copy with both predictions chosen, the p-value line filled, and both stretch answers appended runs clean.
After the whole-number fix, Run all with seed 20261005 gives lean p = 0.0086 (exact 0.0079;
the Monte Carlo SD at 10000 shuffles is about 0.0009),
obese p = 0.341 (exact 0.341), CD8 p = 0.0030 (exact 0.0031), simulated neurons r = 0.23 with p = 0.0009.
Before the fix, the decimal data gave lean p = 0.0059, which an earlier version of this note
wrongly put down to Monte Carlo noise; it was the floating-point bias described under Data.

Independent review, 2026-10-06 (a fresh agent, read-only, against this note, `demo-design.md`, `colab.md`,
the worksheet, and `avoid.md`). Applied:
the whole-number data; the allocation assumption; headings that no longer give away the two predictions;
the obese data shown before its prediction; the large-p answer limited to what the p-value says;
"valid" defined and 1/10001 in the add-one note; "about three times wider";
the second extreme lean split described as a swap; scipy's two-sided default;
"the real labeling should look like any shuffled one"; the lean humps; "mostly the outer humps";
"closer to 0 than 373" instead of a 95% range the students never computed; p about 0.34;
"count mice" instead of a stray `N`; Kafashan et al. cited for removing noise correlations;
the teaser "Each piece has a name" deleted.
Not yet done: opening the notebook from its Colab link in a signed-in browser
(form fields, collapsed answers, both plots, the gates).
