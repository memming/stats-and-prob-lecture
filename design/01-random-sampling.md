# Notebook 1: random sampling and histograms - design

Status: approved 2026-10-05 with two changes,
both applied below:
every unfamiliar call is first shown alone with its raw output,
and the comparison-then-sum in step 3 is split into visible steps.
Implemented in `notebooks/01_random_sampling.py`, paired with `.ipynb` for Colab.
Delivery moved from marimo WebAssembly to Google Colab the same day (see Delivery).
Built from a prior-art survey (see `AGENTS.md`, "Starting a new notebook").

## Where it sits

The first notebook of the course.
It serves the `README.md` objective
"use pseudo-random numbers to simulate probabilistic outcomes"
and prepares the law-of-large-numbers notebook and the loaded-coin exercise.
It stops before running averages (notebook 2),
counts per batch of tosses (sampling distributions, notebook 3),
and deciding whether a die is fair (the exercise).

## Final observation

"How much a histogram looks like the die depends on how many rolls went into it -
far more than I expected."

## Python practice

Drawing samples with numpy's Generator.
Students write `rng.integers(1, 7, size=10)` themselves (step 2),
debug its exclusive upper bound (step 1),
and generalize the same move to `rng.choice(..., p=...)` (step 8).
Everything else they read and run.

## Step ladder

About 15-20 minutes.
Each step lists what is new; at most one new thing per step.
A setup cell creates `rng = np.random.default_rng(20261005)` once;
every later cell draws from it,
so rerunning a cell gives a new sample and a fresh run reproduces every figure.

1. **One roll.** `rng.integers(1, 7)`.
   Run it again (Ctrl/Cmd+Enter) a few times: same answer?
   Quick predict: what can `rng.integers(1, 6)` never return?
   New: the generator, and its exclusive upper bound.
2. **Ten rolls in one call.**
   Rerunning step 1 ten times is tedious, so ask for ten at once.
   Fill one line: `rolls = rng.integers(1, 7, size=10)`, printed below,
   with the step-1 call visible above as the model.
   New: `size=`. Active: write the call.
3. **Count them.** `print(rolls == 3)` first, showing one `True` or `False` per roll;
   then `(rolls == 3).sum()`, checked by eye against the ten printed rolls;
   then a given `for face in range(1, 7):` loop prints the count of every face.
   The same move returns in the hypothesis-test notebook as `(null >= observed).mean()`.
   New: comparison, then sum.
4. **Draw the counts.**
   `plt.hist(rolls, bins=np.arange(0.5, 7))` beside the count table.
   Axes: "face" and "number of rolls".
   Say that each bar holds the rolls between its edges,
   that the bars are the table drawn,
   and that the order of the rolls is gone.
   New: a histogram with explicit bin edges.
5. **Predict, then roll 60.**
   A run is **balanced** if every face came up between 8 and 12 times.
   Prediction first, in a Colab form dropdown:
   "If you do this 60-roll experiment 10 times, how many of the 10 runs will be balanced?"
   The 60-roll cell opens with an `assert` that stops it until a prediction is chosen;
   then rerun it 10 times and tally.
   Answer: about 8% per run; the most and least common faces typically differ by 8 rolls.
   New: the prediction gate. Active: predict.
6. **More rolls.** Draw 6000 rolls once,
   then edit the literal `N` 60 -> 600 -> 6000 to look at the first `N` of them,
   predicting each time whether the shape gets more or less ragged.
   `N` sits in the plot cell, so one rerun updates the figure.
   Only `N` changes between views, not the sample (`colab.md`, fair comparisons).
   Bars switch to proportions (count / N) on a fixed y-axis,
   because raw counts rescale the axis with N and hide the comparison.
   New: proportion. Active: edit and predict.
7. **Name it.** The student first says in their own words what changed
   (collapsed answer below).
   Then the names: these proportions are the empirical distribution;
   the flat level they approach, 1/6, is the probability.
   The formula, proportion of face k = (rolls showing k) / N,
   appears beside the line that already computes it.
8. **Transfer: a flow tube is a loaded four-sided die.**
   `rng.choice(["CD4+", "CD8+", "DN", "DP"], size=n_events, p=[0.59, 0.35, 0.06, 0.01])`,
   the mean of 61 healthy donors (Roszczyk 2024).
   **We hand the simulation the true proportions; a real tube never tells you them.**
   With 100 events the double-positive bar is empty 37% of the time, with 200 still 13%.
   Say that this is a bar chart of categories, not a histogram of a number.
   "You can now simulate any categorical measurement
   and see how many observations its histogram needs before you trust it."
   New: `rng.choice` with `p=`. Active: transfer.

**Stretch (optional):**
- What does `plt.hist(rolls)` draw with its default bins, and why are there gaps?
- What random looks like: type 100 heads and tails yourself,
  then compare your longest run with that of 100 simulated tosses.

Budget: 8 steps, 4 active moments (2, 5, 6, 8),
two kinds of plot (the face histogram in steps 4-6, the category bars in step 8).

Python constructs met, in order:
`default_rng`, `rng.integers` and its exclusive bound, `size=`,
`==` followed by `.sum()`, `plt.hist` with `bins=`, slicing `[:N]`,
division by N, `rng.choice` with `p=`.
Assumed known: `for` loops, `print`, lists and their slices.
Deliberately absent: functions, comprehensions, `np.bincount` (index 0 unused),
`np.unique` (drops faces with zero rolls), data frames.

## Visualization

matplotlib for every plot: its code is what students will reuse on their own data.
Values are shown with `print`, because numpy 2 displays a bare value as `np.int64(2)`.
Altair (an encoding mini-language for one bar chart)
and Plotly (heavier, nothing gained for these plots) were considered and not used.

## Delivery

Decided 2026-10-05: Google Colab.
Students sign in with Google; they used Colab the week before.
The reasons were not speed:
Colab computes on Google's machines, so weak laptops are not a constraint;
students save their work to Drive, which is also a hand-in route;
Jupyter is what they will most likely use on their own data;
and numpy, scipy, pandas, and matplotlib come preinstalled.
Given up: marimo's reactivity (an edited value now needs a rerun of each cell that uses it),
a prediction menu that holds the result back by itself (now a form field plus an `assert`),
and use without sign-in.

Checked in Colab on 2026-10-05 (notebook uploaded to Drive, fresh session):
Run all produced its first output about 11 s after the click, including connecting to a runtime,
and stopped at the prediction gate;
after choosing a prediction, Run all ran to the last cell.
Answers rendered collapsed, with math intact when opened.
The 60-roll plot showed fractional count ticks (2.5, 7.5), fixed with whole-number ticks.

### Superseded: marimo WebAssembly delivery

Kept for the record, in case the course returns to it.
The marimo version is backed up at `~/scratch/tmp/marimo-version-20261005/`.

- matplotlib in an html-wasm `--mode edit` export (marimo 0.25.1):
  about 10 MB more on first load than numpy alone,
  65-96 ms to redraw on a slider keypress.
- A plain-JavaScript anywidget, about 5 MB more, animated rolls dropping into bars
  and drew exactly the counts Python sent it.
- First load downloaded about 37 MB from four hosts
  (jsDelivr 22.6 MB, the marimo interface 11.6 MB, PyPI 2.9 MB, wasm.marimo.app);
  the first plot appeared about 5.5 s after opening on an Apple Silicon Mac,
  of which about 2 s was starting Python in the browser.
- Moving to a second notebook exported into the same folder downloaded nothing
  and plotted in 4.4 s; exported into its own folder, it re-downloaded the 11.3 MB interface.

Delivery findings, tested 2026-10-05 in headless Chromium:

- A plain edit-mode export runs no cell on load:
  students see code and markdown, no outputs, and no prediction menu.
  The exporter always writes `"auto_instantiate": false`,
  and no flag or notebook setting changes it in marimo 0.25.1.
- `--execute` embeds outputs as a static preview,
  but the page is not live: choosing a prediction does nothing until Run all.
- `--execute` plus replacing `"auto_instantiate": false` with `true` in `index.html`
  gives a page that shows outputs immediately and responds to every control.
  The replacement is unofficial and must be re-verified on each marimo upgrade.
- `python -m http.server` failed 2 of 3 cold loads with `ERR_CONNECTION_RESET`
  on marimo's burst of asset requests; a threaded server with a larger listen queue did not.

Decided before the move: students press Run all themselves,
so the export was plain edit mode, neither pre-executed nor patched.
A preview script published it on the PM4MP server:
two cold loads, no failed requests, outputs 1.7 s after Run all.
That server sent no compression or cache headers;
GitHub Pages sends both and serves `.wasm` as `application/wasm`.

## Adopted

| Source | What we took |
|---|---|
| Whitlock & Schluter tutorial, https://www.zoology.ubc.ca/~whitlock/Kingfisher/SamplingNormal.htm | One draw at a time, automated only once it is tedious; controls unlock only when needed; "we know them because it is a computer simulation" |
| GAISE College Report 2016, https://www.amstat.org/docs/default-source/amstat-documents/gaisecollege_full.pdf | Query first; sample one at a time, then stop, then many |
| Coding for Data, https://github.com/odsti/cfd-textbook/blob/main/first_pass_three_girls.Rmd | Rerun by hand until it is boring, then introduce repetition; call out the exclusive upper bound |
| Data 8 ch. 10.1, https://inferentialthinking.com/chapters/10/1/empirical-distributions/index.html | Half-integer bin edges, with the reason stated; the same cell at growing N |
| Data 8 ch. 9, https://inferentialthinking.com/chapters/09/randomness/index.html | "Run the cell several times" as the first act with randomness |
| Rossman/Chance One Proportion, https://www.rossmanchance.com/applets/2021/oneprop/OneProp.htm?candy=1 | Object, then its count, then one mark per result |
| statsthinking21-python, https://github.com/statsthinking21/statsthinking21-python | The sum of a boolean array is a count |
| Crouch et al. 2004, https://doi.org/10.1119/1.1707018; delMas et al. 1999, https://doi.org/10.1080/10691898.1999.12131279; Garfield & Ben-Zvi 2007, https://doi.org/10.1111/j.1751-5823.2007.00029.x | A recorded prediction compared with the result; watching alone barely beats not seeing the demo |
| Tversky & Kahneman 1971, https://doi.org/10.1037/h0031322 | The law of small numbers as the misconception step 5 confronts |
| Kaplan et al. 2014, https://doi.org/10.1080/10691898.2014.11889701; delMas et al. 2007, https://doi.org/10.52041/serj.v6i2.483 | The first histogram shows a number (die face), not categories; build it from the raw rolls; say the order is discarded |
| Cooper & Shore 2008, https://doi.org/10.1080/10691898.2008.11889559 | No talk of "variability" over a flat histogram, which students misread as low variability |
| Schilling 1990, https://doi.org/10.1080/07468342.1990.11973306 | Longest-run stretch exercise |
| Roszczyk et al. 2024, https://doi.org/10.5114/ceji.2024.136371 | CD4/CD8/DN/DP proportions among CD3+ cells, mean of 61 healthy donors |

## Rejected

| Source | What | Why |
|---|---|---|
| Seeing Theory, https://seeing-theory.brown.edu/basic-probability/index.html | True probabilities beside the data, "bound to get closer and closer to 50%" before any flip | Conclusion before phenomenon; observed bars have no y-axis or N; no prediction; unmaintained since 2019 |
| Art of Stat Random Numbers, https://istats.shinyapps.io/RandomNumbers/ | Three bar charts for one idea; "Fix Random Seed" checkbox | Plot carries several ideas; a fixed seed makes every rerun identical |
| Rossman/Chance candy applet (above); StatKey, https://www.lock5stat.com/StatKey/sampling_1_cat/sampling_1_cat.html | Every control on screen at once | A dashboard; knobs must arrive one at a time |
| Data 8 ch. 10.1 (above); Whitlock tutorial (above) | Probability histogram or population curve shown before any sample | Truth before phenomenon |
| Data 8 ch. 9.3, https://inferentialthinking.com/chapters/09/3/simulation/index.html; Data 8 lab06, https://github.com/data-8/materials-sp26 | A function, a loop and `np.append` before the concept; `np.random.seed` in the fill-in cell for the autograder | Programming as a second subject; reruns identical |
| marimo-team/learn probability notebooks, https://github.com/marimo-team/learn | `np.random.seed(42)` in the drawing cell; concept code hidden with `hide_code`; annotated multi-idea plots; slider where a literal would do | Reruns identical; hides the computation; plots carry several ideas |
| Neuromatch Academy W0D5, https://github.com/NeuromatchAcademy/precourse | Six distributions in one tutorial; seed in rerun cells; two or three sliders at once; 120 hidden plotting lines; solutions as external links | One idea per notebook; reruns identical; dashboard; answers must sit collapsed in place |
| risk-engineering, https://risk-engineering.org/notebook/coins-dice.html | numpy, scipy.stats and sympy for one idea; a sampler called once per draw in a loop | Three libraries; about 1.3 s per 10k draws natively, worse in Pyodide |
| UBC Python probability, https://ubcmath.github.io/python/probability/discrete.html | Factorials and binomial coefficients first | Formula before phenomenon |
| Seen across sources | `plt.hist` with default bins on die faces | Gaps between faces, 5 and 6 side by side |
| Deitel RollDie, https://github.com/pdeitel/PythonFundamentals2e/blob/main/examples/05/RollDie.py | `np.unique(..., return_counts=True)` for counts | Silently drops faces nobody rolled, exactly when N is small |
| Last year's Day 1 activity 1, `old_ref/Day1 activity/Day1_activity1_probability_v1.3.ipynb` | Global `numpy.random` (`random.rand()`); seaborn `histplot`; helper functions `sample_uniform` and `coin_toss` before the concept; a continuous uniform as the first object | Legacy global generator; an extra library; programming as a second subject; the first histogram should count a number students can hold (die faces) |
| Last year's Day 2 activity 1, `old_ref/Day2 activity/Day2_activity1_probability_v1.1.ipynb` | Six distributions in one notebook | One idea per notebook |

Kept from last year's Day 1 activity 1 (local, `old_ref/`):
"save a copy before you proceed" as the first instruction,
"run it again" as the first act with randomness,
and `<details>` solutions, which rendered in Colab for that class.

## Deferred to later notebooks

- Law of small numbers with coins: exactly 5 heads in 10 tosses 24.6%, exactly 50 in 100 about 8% (notebook 2 or 3).
- International Brain Laboratory stimulus side, 50/50 then unsignaled 80/20 blocks,
  https://doi.org/10.7554/eLife.63711: the loaded-coin exercise.
  Mendel's 705 purple of 929 against 75% (Data 8 ch. 11.3) as a second case.
- Synaptic release site as a coin, p from 0.09 to 0.54 across terminals,
  https://doi.org/10.1126/science.7901909; sites are not independent under paired pulses.
- CheckMate 067 response rates, https://doi.org/10.1056/NEJMoa1504030, for hypothesis tests and power.
- Small open datasets, to be bundled in the repo (some hosts send no CORS header):
  Sipe et al. 2022 tumor volumes (CC0), https://zenodo.org/records/6858951;
  Kramer & Eden retinal spikes (MIT), https://github.com/Mark-Kramer/Case-Studies-Python;
  Riaz et al. 2017 nivolumab response (ODbL, share-alike) via cBioPortal.
- Gambler's-fallacy trap: averaging per-sequence proportions is biased; pool counts
  (Miller & Sanjurjo 2018, https://doi.org/10.3982/ECTA14943).

## Decisions

Approved 2026-10-05; the alternative not taken follows each.

1. Die only in this notebook, coins from notebook 2 on
   (not: a coin first, as the README sketch says).
2. A prediction menu that holds back the result until a value is chosen
   (not: a printed "predict" prompt only).
   In Colab: a form dropdown, and an `assert` opening the result cell.
3. `plt.hist` with explicit edges in step 4 (not: `plt.bar` over the count table).
4. Transfer: the flow-cytometry die as the core step, the synapse coin as stretch
   (not: the reverse).
