# Notebook 2: averages - the law of large numbers and the central limit theorem - design

Status: approved 2026-10-05, about 15 minutes, with "a bit of elaboration" allowed.
The first draft (law of large numbers only, 8 steps) was judged a bit heavy;
Memming asked for the law of large numbers and the central limit theorem together.
Open decisions taken at their recommended defaults (see Decisions).
Implemented in `notebooks/02_averages.py`, paired with `.ipynb` for Colab.
Elaboration added beyond the ladder: a collapsed "Why the square root?" note
(variances of independent draws add) and a paragraph on why the bell matters
for error bars and later tests.
Built from a prior-art survey (see `AGENTS.md`, "Starting a new notebook"):
`old_ref/` and its books, interactive tools and courses, misconception research,
and examples from neuroscience and cancer immunology.

## Where it sits

The second notebook.
Notebook 1 ended: "Why it converges, and how fast, is the subject of the next notebook",
and its step-6 answer promised that ten times more rolls gives about three times less raggedness.
This notebook pays both off.
It serves the `README.md` objective "apply the law of large numbers to averages",
and covers the `README.md` section "Central limit theorem and Law of large numbers".
Notebook 3, "Sampling distribution of the mean", now starts from the bell this notebook shows;
what it adds is to be decided when it is designed.

## Final observation

"Averages of many tosses pile up in a bell around the true value,
whatever a single toss looks like,
and four times more tosses make the bell half as wide."

## Python practice

Repeating an experiment many times in one call:
`rng.integers(0, 2, size=(runs, N))`, one row per run, then `.mean(axis=1)`, one average per run.
Students write the `size=(runs, N)` call themselves (step 3).
Later notebooks (sampling distributions, shuffling) reuse exactly this move.

## Step ladder

About 15-20 minutes.
At most one new thing per step.
A setup cell creates `rng = np.random.default_rng(20261005)` once.
Two knobs are named and kept apart throughout:
`N`, the tosses in one run, and `runs`, how many times we repeat the run, fixed at 10000.
The same three run lengths, N = 4, 16, 64, appear in every step,
each four times the last.

1. **A proportion is an average.**
   Ten tosses as 0s and 1s (`rng.integers(0, 2, size=10)`), printed;
   then `tosses.mean()`, which is the proportion of heads.
   Links to notebook 1: its bar heights were averages of 0s and 1s.
   New: `.mean()`.
2. **One row per run.**
   `rng.integers(0, 2, size=(5, 4))` printed: five runs of 4 tosses.
   Then `.mean()` (one number for the whole table)
   and `.mean(axis=1)` (one average per run), both printed raw.
   New: a 2-D `size` and `axis=1`.
3. **Lopsided runs: predict, then count.**
   Let's call a run **lopsided** if at least 3 in 4 of its tosses are heads.
   Form dropdown, with the `assert` gate from notebook 1:
   "Which is more likely to be lopsided: a run of 4 tosses or a run of 16?"
   (options: 4 tosses / 16 tosses / about the same).
   Students write the `size=(runs, 16)` call, with the N = 4 line as the model;
   `(means >= 0.75).mean()` gives the fraction of lopsided runs.
   Answer: about 31% (5 in 16) of 4-toss runs, about 4% of 16-toss runs.
   New: the extreme-case contrast. Active: predict, write the call.
4. **The shape of the averages.**
   Predict first: "What will the averages of 64 tosses look like?"
   One figure, three histograms on one shared axis,
   the 10000 averages for N = 4, 16, 64,
   with notebook 1's half-integer edges divided by N.
   The averages crowd toward 0.5 (law of large numbers)
   and take a bell shape (central limit theorem),
   although a single toss has only two possible values.
   New: a histogram of averages. Active: predict.
5. **How fast the bell narrows.**
   Predict: "each time N is multiplied by 4, what happens to the width?"
   Then print the spread of the averages (`means.std()`) for N = 4, 16, 64:
   0.25, 0.125, 0.0625 - it halves each time.
   `.std()` is described in words as the square root of the variance,
   the average squared distance from the mean,
   so the "finite variance" of step 6 and the "variances add" note are defined before use.
   New: `.std()`. Active: predict.
6. **Name it.**
   The student says in their own words what happened as N grew (collapsed answer).
   Then the names:
   the **law of large numbers** (the average of many independent draws settles at the true value),
   the **central limit theorem** (those averages are approximately normally distributed,
   whatever one draw looks like),
   and the **square-root law** (their spread is sigma/sqrt(N); sigma = 0.5 for one toss).
   The formula appears beside the measured spreads from step 5.
   This spread is the **standard error**, the SE on students' error bars;
   the spread of single values is the **standard deviation**.
7. **Worked example: averaging EEG trials, and why we average.**
   One cell, `n_trials` editable.
   One trial's P3 amplitude: `rng.normal(6, 5, size=(runs, n_trials))`, in microvolts.
   **For teaching purposes, the simulation gets an assumed true amplitude and noise**,
   approximately those of real oddball data:
   single-trial SD about 5 uV (Luck et al. 2021), P3 effect about 6 uV (ERP CORE).
   The cell prints the SD of single trials (about 5) and the SE of the average (about 5/sqrt(n_trials)).
   Edit `n_trials`: how many trials bring the SE to 0.5 uV? (100.)
   Close: averaging N independent measurements shrinks their noise by sqrt(N),
   and only if they are independent;
   for a claim about people, N counts people, not trials (Boudewyn et al. 2018).
   New: `rng.normal`. Active: edit.

**Stretch (optional):**
- **Diluted, not corrected.**
  Five sequences of 100000 tosses; at N = 10, 1000, 100000 print
  the excess heads (`heads - N/2`) and the proportion of heads.
  The proportion settles while the excess typically grows (about 1, 13, 127):
  early luck is diluted, not corrected, so tails are never "due".
- **More mice, not more calipers.**
  Tumor volume per mouse varies a lot (SD about 740 mm^3 around 1270; Sipe et al. 2022, CC0 data);
  repeated caliper readings of one tumor vary about 14% (Jensen et al. 2008).
  Measuring each mouse 3 times barely changes the error of the group mean;
  twice as many mice cuts it by 29%.
  Technical replicates average out only the measurement noise (Vaux, Fidler and Cumming 2012).

Budget: 7 steps, 4 active moments (3, 4, 5, 7), one figure (step 4).

Python constructs met, in order:
`.mean()`, 2-D `size=(runs, N)`, `axis=1`, `>=` then `.mean()` (notebook 1's move),
`plt.subplot(3, 1, row)` with a row counter for three stacked histograms
(not `plt.subplots`, `zip`, or `enumerate`, which would be new), `.std()`, `rng.normal`.
The figure's markdown says each panel has its own vertical scale:
narrower bins hold fewer runs, so peak heights fall as `N` grows; compare widths.
Assumed known: `for` loops, lists, `print`, f-strings, half-integer bin edges (notebook 1).
Deliberately absent: `np.cumsum` running averages
(the evidence favors fixed-N contrasts, and it would be a new construct);
a fitted normal curve over the histograms (one more formula and library for little gain).

## Visualization

Printed numbers everywhere except step 4:
three stacked histograms of averages on one shared x-axis,
so narrowing and the bell are both visible.
N = 1 is left out of that figure: its two bars, each a full unit wide,
would extend from -0.5 to 1.5 and suggest impossible proportions.
No running-average paths with plus-or-minus bands:
a single path keeps crossing such a band, which invites misreading it as a wall.

## Adopted

| Source | What we took |
|---|---|
| Dekking et al., *A Modern Introduction to Probability and Statistics*, ch. 13, pp. 188-189 (`old_ref/books/`) | A relative frequency is the average of 0/1 indicators (step 1) |
| Simon, *Resampling: The New Statistics*, ch. 24, pp. 390-391 (`old_ref/books/02_resampling_book/`); open edition https://github.com/resampling-stats/resampling-with | Quadruple the sample to halve the error, as a predict-then-check (step 5); "the law of averages" and "due" as the misconception to confront (stretch) |
| Kass et al., *Analysis of Neural Data*, pp. 139-145 (`old_ref/books/`) | The name "square-root law"; the law of large numbers collapses the averages onto the truth while the central limit theorem describes their shape (step 6); independence is required (step 7) |
| Lane, Online Statistics Education, Gambler's Fallacy, https://onlinestatbook.com/2/probability/gambler.html | Excess count beside proportion from the same tosses (stretch) |
| Data 8 ch. 14.5, https://inferentialthinking.com/chapters/14/5/variability-of-the-sample-mean/index.html | Measured spread of averages beside the formula, formula only after the simulation (steps 5, 6) |
| MIT 18.05 reading 6b, https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/mit18_05_s22_class06-prep-b.pdf | The law of large numbers as "the fraction of runs within a tolerance" (step 3) |
| Downey, *Think Stats*, ch. 8, https://github.com/AllenDowney/ThinkStats | SD describes individuals, SE describes how precise an average is (step 6) |
| Sommerhoff, Weixler and Hamedinger 2022, https://doi.org/10.1007/s13138-022-00213-x | Open on an extreme case at two fixed sizes, not a running path (step 3) |
| Bishop, Thompson and Parker 2022, https://doi.org/10.1098/rsos.211028; Fong, Krantz and Nisbett 1986, https://doi.org/10.1016/0010-0285(86)90001-0 | Simulation alone does not transfer; state the rule explicitly (step 6) |
| Watkins, Bargagliotti and Franklin 2014, https://doi.org/10.1080/10691898.2014.11889716; Lane 2015, https://doi.org/10.1080/10691898.2015.11889738 | Keep N and the number of runs apart, with runs fixed and large |
| Falk and Lavie Lann 2015, https://doi.org/10.1111/test.12031; Dinov, Christou and Gould 2009, https://doi.org/10.1080/10691898.2009.11889499 | Counts drift apart while proportions settle (stretch) |
| Belia et al. 2005, https://doi.org/10.1037/1082-989X.10.4.389; Zhang et al. 2023, https://doi.org/10.1073/pnas.2302491120 | Researchers misread SE bars; print the SD of single trials beside the SE of the average (step 7) |
| Luck et al. 2021, https://doi.org/10.1111/psyp.13793; Kappenman et al. 2021 (ERP CORE), https://doi.org/10.1016/j.neuroimage.2020.117465; Boudewyn et al. 2018, https://doi.org/10.1111/psyp.13049 | ERP single-trial noise and P3 size; sqrt(N) stated for ERPs; trials vs participants (step 7) |
| Sipe et al. 2022, https://doi.org/10.7554/eLife.79143, data https://zenodo.org/records/6858951 (CC0); Jensen et al. 2008, https://doi.org/10.1186/1471-2342-8-16; Vaux, Fidler and Cumming 2012, https://doi.org/10.1038/embor.2012.36 | Mice vs caliper readings: biological vs technical replicates (stretch) |

## Rejected

| Source | What | Why |
|---|---|---|
| Seeing Theory, Expectation, https://seeing-theory.brown.edu/basic-probability/index.html | "Watch as the running sample mean converges to 3.5" before any roll; one path | Truth before phenomenon; one path cannot show spread at fixed N |
| Lane, sampling distribution demo, https://onlinestatbook.com/simulations/sampling_dist_N/step.html | Population, two N, mean/median switch and a draggable bar on one screen; N = 2, 5, 10, 15, 25 | A dashboard; non-geometric N hides the ratio |
| Data 8 ch. 14.5 (above) | n = 25..625 | Hides the ratio between sizes |
| Chan, *Probability for Data Science* 6.3, https://probability4datascience.com/eBook/ch06-3.html | Plus-or-minus 3 SE bands drawn over running paths | Reads as a wall a path stays inside; a single path keeps crossing it |
| Davidson-Pilon, *Bayesian Methods for Hackers* ch. 4, https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers | Formula first; linear N axis clipped to a narrow y range; `norm(mean, 1./std)` bug | Truth before phenomenon; the rate is invisible; a wrong SD |
| QuantEcon, https://intro.quantecon.org/lln_clt.html; Neuromatch W0D5, https://github.com/NeuromatchAcademy/precourse | Theorem stated first; prefix-mean loop; reseeding inside a hidden form cell | Truth first; loops where one call does; reruns identical |
| Last year's notebooks, `old_ref/Day1 activity/Day1_activity2_monty_hall_v1.1.ipynb`, `old_ref/Day2 activity/Day2_activity1_probability_v1.1.ipynb`, `old_ref/Day4 activity/Day4_activity1_hypothesis_testing_v1.1.ipynb` | Running mean inside about 60 lines of hidden widget code; theoretical mean printed beside every result; global seeds; a normal curve with sigma/sqrt(n) before any sampling; Day 4 bugs (an n = 10 plot labelled n = 5; low means never rejected) | Hides the computation; truth first; reruns identical |
| Simon, ch. 21, p. 323 | Calls the central limit theorem the "Law of Large Numbers" | Conflates the two results this notebook names separately |

## Deferred to later notebooks

- Dekking fig. 14.1: scaling (mean - mu) by n^(1/4), n^(1/2), n, where only sqrt(n) keeps the shape;
  MIT 18.05's "more than 55 of 100 vs more than 220 of 400" question;
  last year's Day 4 lognormal cell-diameter population (a skewed population whose averages still form a bell).
- Real spike counts: Kass example 3.4 (60 M1 counts, Matsuzaka et al. 2007), printed in the book;
  the source's terms must be checked before use.
  Kramer and Eden retinal spikes (MIT; correlated bins slow convergence).
- Kramer and Eden `02_EEG-1.mat` (MIT): 1000 trials per condition,
  but its noise is white Gaussian, so it is probably simulated; label it so if used.
- Correlated neurons cap the benefit of averaging (Kass example 6.1, Shadlen and Newsome; rho about 0.12).
- *Bayesian Methods for Hackers*' "disorder of small numbers" funnel (extremes come from small units).

## Decisions

Taken 2026-10-05 at the recommended defaults; the alternative not taken follows each.

1. Coin tosses as 0/1: a proportion is an average, and the loaded-coin exercise follows
   (not: notebook 1's die, whose averages settle at 3.5).
2. Spread measured as the standard deviation of the averages, named the standard error in step 6
   (not: Simon's average distance from the truth, which avoids SD but does not connect to SE bars).
3. EEG trial averaging as the core worked example, tumor volumes (mice vs calipers) as stretch
   (not: the reverse).
4. The fill-in for 16-toss runs is a blank `...`, which errors until filled,
   rather than an editable copy of the 4-toss line:
   an unedited copy would print the 4-toss answer under the 16-toss label
   and seem to confirm "about the same".
