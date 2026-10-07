# Notebook 7: power - how many mice to plan for - design

Status: approved 2026-10-07 ("ok. let's try"), every decision at its default; implemented the same day in `notebooks/07_power.py`, paired with `.ipynb` for Colab. Numbered 07 after merging the Day 2 afternoon notebooks 04-06.
Ported from last year's Day 4 activity 3 (`old_ref/Day4 activity/Day4_activity3_power_analysis_v1.1.ipynb`),
redesigned rather than translated (see Rejected).
Built from a prior-art survey (see `AGENTS.md`, "Starting a new notebook"):
`old_ref/` and its books, interactive tools, Python notebooks, courses, GitHub,
misconception research, methods sources for animal experiments,
and open data from neuroscience and cancer immunology.

## Where it sits

Day 3 morning, first; notebook 8 (experimental design) follows.
Memming explains power in the lecture; this notebook writes the formal definition down
and turns it into a plan.

What students have met before it:
- The coin worksheet (`worksheets/coin_test.tex`):
  alpha as the 1-in-20 limit, the Type I error,
  and, at the board, power: a coin landing heads 70% of the time is accused only about 15% of the time in 10 flips;
  "more flips would raise it, which leads to sample-size planning on Day 3".
- Notebook 3: the shuffle test on 5 vs 5 mice;
  the obese mice gave p about 0.34, and the answer ended
  "five mice per group cannot tell a modest effect from none".
- Day 2 afternoon, by Hyungju Jeon (merged 2026-10-07 from PRs #3-#5):
  notebook 4 reads an AI-written `permutation_test(a, b, ...)`;
  notebook 5 computes the power curve of the coin rule against the coin's bias,
  the alpha-beta trade-off, and the effect of more flips (optional: winner's curse, peeking);
  notebook 6 runs `my_test` on fake splits of saline mice
  (about 5% significant with one mean per mouse, about 47% when each reading counts).
- Functions (`def`, arguments, `return`, scope):
  Computational Thinking, "Functions 1" and "Functions 2", 2026-09-29.

What it adds to notebook 5:
notebook 5 fixed a rule and asked how often it accuses coins of different bias.
This notebook asks the question a student faces before an experiment: how many mice?
New are a measurement that varies from mouse to mouse in two groups,
an effect chosen before the experiment (the smallest worth finding)
with a spread borrowed from earlier experiments,
the test one will actually run inside the simulation,
and reading the number of mice off a curve.

It serves the `README.md` objectives
"Calculate required sample size through power analysis"
and "Use sampling distributions to describe p-value and statistical power",
and starts "Design an experiment's sample size and write a practical protocol for approval",
which notebook 8 finishes.

## Final observation

"Simulating the planned experiment many times shows how many mice it needs to catch an effect worth finding."

## Python practice

Wrapping notebook 3's shuffle loop in a function, `shuffle_test(control, treated)`, that returns the p-value,
and calling it once per simulated experiment inside a second loop.
Students fill `power = (p_values <= 0.05).mean()`,
notebook 3's compare-then-average move one level up:
a p-value counts shuffles, power counts experiments.

## Data

**Core: fear conditioning, field-typical numbers.**
Carneiro et al. 2018, PLOS ONE 13:e0196258, https://doi.org/10.1371/journal.pone.0196258, CC BY 4.0.
S1 Data is an Access database of 410 control-vs-treated comparisons from 122 articles
(group mean freezing, SEM, n; the unit is the animal).
Recomputed from S1 Data on 2026-10-07:
median n per group 10 (IQR 8-12, 336 comparisons with exact n),
median freezing of the higher group 50%, median pooled SD/mean 0.43, median control SD 16.1 points.
The paper's "intermediate" typical effect is a 37.2% reduction in freezing
(the mean of well-powered experiments), and it states:
"around 15 animals per group are needed to achieve 80% power",
a number "reached in only 12.2% of cases ... as most experiments had sample sizes of 8 to 12";
one article of 122 reported a sample-size calculation.
Typical experiment: 50% vs 31.4% freezing, SD 17.4, d = 1.07, 14.8 per group (t-test, statsmodels).

The notebook uses: control mice freeze 50% of the time on average, SD 17 points from mouse to mouse;
the drug worth finding lowers this to 31% (a difference of 19 points).
These summarize a field, not one experiment, and the notebook says so.
Each simulated mouse is a draw from a normal distribution with these true values,
**handed to the simulation, which a real lab never knows**; the notebook says this in bold.
A normal(31, 17) mouse falls below 0% freezing with probability 0.034 (about 1 in 30);
clipping to 0-100% changed power by under 0.02 at n = 5, 10, 15 (2000 experiments each),
within Monte Carlo error.

**Transfer: the obese mice of notebook 3.**
Sipe et al. 2022, eLife 11:e79143, Figure 5B (CC0): obese control volumes have mean 2475 mm^3 and SD 1162 (5 mice).
The notebook rounds to 2500 and 1200 and plans for a 300 mm^3 (12%) difference.
A normal(2200, 1200) volume is negative with probability 0.033, the same order as the freezing model.
The paper's only sample-size sentence: "Sample size was determined by power analysis calculations and pilot experiments."
A separate untreated obese cohort in the same paper (Figure 1E, 17 mice) has SD/mean 0.58, against 0.47 here:
the spread estimate itself is uncertain (rigor point 5).

**Numbers**, verified 2026-10-07 with the notebook's `shuffle_test`
(two-sided, 1000 shuffles, ties counted with `- 1e-9`, see "Found while implementing")
and seed 20261008, so that they do not depend on the notebook's own seed;
2000 simulated experiments per point unless stated.
"t" is the noncentral-t power of a two-sided t-test, for comparison.

| Scenario | n per group | Shuffle-test power | t-test power |
|---|---|---|---|
| Freezing 50 vs 31, SD 17 | 5 / 10 / 12 / 14 / 15 / 20 / 30 | 0.32 / 0.66 / 0.76 / 0.82 / 0.84 / 0.94 / 0.99 | 0.34 / 0.66 / 0.74 / 0.81 / 0.84 / 0.93 / 0.99 |
| No effect, 50 vs 50 (4000 experiments) | 5 / 10 | 0.051 / 0.049 | - |
| Fixed budget, n = 10, drug mean 40 / 35 / 30 / 28 / 25 | 10 | 0.25 / 0.46 / 0.71 / 0.79 / 0.87 | - |
| Obese, 2500 vs 2200, SD 1200 (600 experiments; n = 5: 4000) | 5 / 200 / 250 / 300 | 0.059 / 0.70 / 0.75 / 0.87 | 0.06 / 0.70 / 0.80 / - |

Half the effect, 50 vs 40.5, before the tolerance fix (500 experiments): 0.24 / 0.39 / 0.71 / 0.87 at n = 10 / 20 / 40 / 60,
against t 0.22 / 0.41 / 0.69 / 0.86.
80% power: about 14 mice per group for the full effect, about 55 for half of it, about 250-270 for the obese transfer.
At n = 5 the obese experiment had about 6% power to detect 300 mm^3.
The shuffle test sits below the t-test at n = 5 (0.32 against 0.34):
with 252 splits its two-sided rejection region holds at most 12, an exact level of 0.048.
Winner's curse: among experiments that detected the drug,
the average observed difference was 28.8 at n = 5, 22.9 at 10, 20.7 at 15, 19.0 at 30 (true 19).
Clipping freezing to 0-100% changed power by under 0.02 (n = 5, 10, 15; 2000 experiments, before the tolerance fix);
clipping tumor volumes at 0 raised the obese power by 0.01-0.05 at n = 200-300 (600 experiments each, within about 2 SE),
so the notebook makes the "barely changes" claim only for freezing.
Speed, measured locally on Apple Silicon: 1000 experiments x 1000 shuffles take 2.3 s at n = 5;
the five-point sweep at 500 experiments about 6 s; the obese sweep at 300 experiments about 5 s.
Colab is not measured; expect two to five times slower.

## Rigor: what the notebook states, and the sources

1. **Definition.** For a test that rejects the null hypothesis when p <= alpha,
   with n mice per group and true difference delta between the group means,
   power(delta, n) = P_delta(p <= alpha) = E_delta[1{p <= alpha}],
   and the Type II error rate is beta = 1 - power(delta, n).
   At delta = 0 the same probability is the Type I error rate, at most alpha.
   Power is a function of delta, n, the spread, alpha, and the test, not one number
   (the pilot finding in Hyungju's `design/05-errors-and-power.md`: every AI tested gave beta as one number).
   Written in expectation notation per the course diary of 2026-10-06 (`diary/2026-10-06.md`).
2. **The simulation estimates it.** The fraction of M simulated experiments that reject
   is the sample mean of M indicators, so its SD is sqrt(power (1 - power) / M) <= 0.5 / sqrt(M):
   at most 0.016 for M = 1000 and 0.022 for M = 500 (notebook 2's spread of an average).
   The test uses notebook 3's plain fraction of 1000 shuffles;
   compared with the always-valid (1 + b)/(1 + B), it rejects at one more count (b = 50),
   so its Type I error rate can exceed alpha by at most about 0.001.
3. **Lehr's rule.** n = 16 / Delta^2 per group, Delta = (mu0 - mu1) / sigma,
   for a two-sided alpha = 0.05 and power 0.80, normal data with equal SDs;
   16 rounds 2 (z_0.975 + z_0.80)^2 = 15.68
   (van Belle, 2008, Sec. 2.1, Eqs. 2.3-2.5, pp. 29-30;
   free chapter: http://www.vanbelle.org/chapters/webchapter2.pdf).
   Here 16 (17/19)^2 = 12.8; the simulation needs about 14, because the rule treats sigma as known.
   Halving delta multiplies n by four.
4. **Power is for planning.** The power of a finished experiment computed at its own observed difference
   is a one-to-one function of its p-value and adds nothing to it
   (Hoenig & Heisey, 2001, Sec. 2.1; Lakens, 2022; Greenland et al., 2016, items 24-25).
5. **Choose delta as the smallest difference worth finding**, not as a small pilot's estimate,
   and distrust a spread estimated from a handful of animals
   (NC3Rs Experimental Design Assistant, https://eda.nc3rs.org.uk/experimental-design-group;
   Percie du Sert, Ahluwalia, et al., 2020, item 2:
   "Pilot studies alone are unlikely to provide adequate data on variability for a power calculation";
   Lakens, 2022, "Using an estimate from a previous study"; Albers & Lakens, 2018).
   The same document gives the target power the notebook states:
   "A target power between 80% and 95% is normally deemed acceptable".
6. **Small significant experiments exaggerate.** Among experiments that reach p <= 0.05,
   the observed difference overstates the true one, most at low power
   (Button et al., 2013, p. 366; Gelman & Carlin, 2014; Loken & Gelman, 2017).
   Button et al. (2013) estimate "the median statistical power in neuroscience is 21%".

## Step ladder

About 15 minutes, plus under a minute of computing in Colab (not measured).
At most one new thing per step.
A setup cell creates `rng = np.random.default_rng(20261007)` once.

1. **The test from notebook 3, as a function.**
   `np.concatenate([control, treated])` printed raw on notebook 3's lean mice, split into two arrays.
   Then `def shuffle_test(control, treated):` holding notebook 3's loop, 1000 shuffles,
   counting both directions ("as most papers do, and as published sample sizes assume"),
   returning the p-value.
   Run on the lean mice: about 0.016, notebook 3's two-sided answer (exactly 4/252).
   New: `np.concatenate`; the loop inside a function (`def` is known).
2. **One planned experiment, simulated.**
   The plan: does a drug given after fear conditioning weaken the memory?
   Mice freeze when they recall the shock; Carneiro et al.'s numbers as above.
   Bold: here we play nature, handing the simulation the true means and SD.
   `n = 5`, `control = rng.normal(50, 17, size=n)`, `treated = rng.normal(31, 17, size=n)`,
   both printed rounded, then `print(shuffle_test(control, treated))`.
   Run the cell again a few times: does the test detect the drug every time?
   Collapsed answer: no; p jumps from below 0.01 to above 0.5 although the drug works in every run.
   New: a simulated experiment with an effect built in. Active: rerun.
3. **Predict, then 1000 experiments.**
   Form dropdown with the `assert` gate: "Of 1000 such experiments with 5 mice per group,
   how many detect the drug (p <= 0.05)?" (almost all / about two thirds / about one third / almost none).
   A loop collects 1000 p-values, then `p_values = np.array(p_values)`.
   Students fill `power = ...` with `(p_values <= 0.05).mean()`.
   Collapsed answer: about 0.33; researchers guess high too (Bakker et al., 2016).
   Every experiment that missed had the same real drug:
   "not significant" here never means "no effect" (Greenland et al. 2016, items 4 and 8).
   New: none beyond counting experiments. Active: predict, fill one line.
4. **More mice, more often.**
   Form dropdown: "How many mice per group detect the drug in 80% of experiments?" (about 8 / 15 / 30 / 60).
   A loop over `n_values = [5, 10, 15, 20, 30]`, 500 experiments each, collects one power per n;
   plot power against mice per group, with a dashed line at 0.8.
   Collapsed answer: about 14 per group; the field's usual 8-12 detect a typical drug about 55-75% of the time (t-test: 0.55 at 8, 0.74 at 12),
   and Carneiro et al. found 15 or more per group in 12.2% of experiments.
   New: a loop over n around the loop over experiments; the power curve. Active: predict.
5. **Name it.**
   The student says what the simulation showed (collapsed answer).
   Names: **power**, the **Type II error** and **beta** = 1 - power,
   **sample-size planning** (a-priori power analysis).
   The definition (rigor point 1), beside the line that computes it:
   the fraction is the sample mean of indicators, an estimate of the expectation, give or take 0.02 (point 2).
   A collapsed "Check (optional)": set 31 to 50 in step 3's cell and rerun; about 0.05, the Type I error rate.
   The formula: n = 16 sigma^2 / delta^2 per group (point 3), 12.8 here;
   halving the difference worth finding needs four times the mice (about 55 by simulation).
   The planning list: the smallest difference worth finding, a spread from earlier experiments,
   alpha and the direction, the test, a target power (80-95%), and the n they give.
   Animal-research reports are asked to explain how the sample size was determined (Percie du Sert, Ahluwalia, et al., 2020, item 2).
   **For deeper mathematics:** van Belle ch. 2; Lakens 2022.
6. **Worked transfer: the obese mice of notebook 3.**
   Plan the next obese experiment: the smallest difference worth finding is 300 mm^3,
   the SD from notebook 3's five control mice is about 1200 mm^3.
   Prose prediction from the formula (16 x (1200/300)^2 = 256), then one cell repeating step 4
   with these values, `n_values = [50, 100, 200, 300]` and 300 experiments each, and the same plot.
   Collapsed answer: about 250 per group; five mice detect it about 6% of the time.
   This is not "the power of notebook 3's experiment": a finished experiment's power at its own difference
   restates its p-value (point 4). And the 1200 comes from five mice; a separate cohort in the same paper
   suggests a different spread (point 5).
   New: none. Active: predict, run.
7. **You can now ...**
   plan how many mice an experiment needs:
   simulate the experiment you plan with the smallest effect worth finding,
   run the test you will run, count, and raise n until the fraction is high enough.
   For the t-test, `statsmodels.stats.power.TTestIndPower` and G*Power do it in one call;
   the simulation works for any test.
   Caveats, one sentence each: power is for planning (point 4);
   small significant experiments overstate the effect (point 6);
   median power in neuroscience was about 21% (Button et al. 2013).
   Last, in one plain sentence:
   "Power is the fraction of planned experiments that would catch the effect; choose the number of mice that makes it high."

**Stretch (optional):**
- **Lucky experiments exaggerate.** Record the observed difference in step 3's loop too;
  average it over the experiments that detected the drug: about 29 at n = 5, against the true 19;
  rerun at n = 30: about 19.4. Links to notebook 5's optional winner's-curse question.
- **A fixed budget.** With 10 mice per group, which differences are detected 80% of the time?
  Loop over the difference instead of n (the sensitivity analysis of Lakens 2022).

Budget: 7 steps, 4 active moments (2, 3, 4, 6), two plots of the same form (steps 4 and 6).

Python constructs met, in order:
`np.concatenate`, `def` with `return`, `rng.normal(mean, sd, size=n)` (notebook 2), `round` for printing,
a loop collecting p-values, `<=` then `.mean()`, a loop around a loop, `plt.plot` with `plt.axhline` (notebook 1).
Assumed known: functions, loops, lists, form dropdowns and the `assert` gate.
Deliberately absent: `scipy.stats.ttest_ind` and `statsmodels` on the core path (named in step 7),
Cohen's d as an axis or a knob (the axis is in freezing points),
`while power < 0.8` searches, and any widget.

## Visualization

One plot form, used twice: power against mice per group, points joined by lines,
a dashed horizontal line at 0.8, y from 0 to 1,
x "mice per group", y "fraction of experiments that detect the drug".
The obese transfer has its own x-scale (50-300 mice).
No histogram of p-values or of observed differences on the core path:
each would add a second object to read (see Rejected).

## Adopted

| Source | What we took |
|---|---|
| Simon, *Resampling: The New Statistics*, ch. 24 "How Large a Sample?", Ex. 24-4 (pigs), pp. 403-405 (`old_ref/books/02_resampling_book/`); open edition, Simon and Brett, *Resampling with*, ch. 30, https://resampling-stats.github.io/latest-python/how_big_sample.html | "The first step is to guess the results": the model is a stated guess (steps 2, 6); the simulated universe with the effect built in |
| PH525, "Power calculations", https://genomicsclass.github.io/book/pages/power_calculations.html | One simulated experiment returns a test result, averaged over many runs; power against N as the plot (steps 3, 4) |
| Oxford StatsCourseBook 2024, 2.4.6 and 2.4.9, https://jillxoreilly.github.io/StatsCourseBook_2024/2.4_Power/2.4.6_PowerCorrelationSim.html | The null check with the same loop; the 80% reference line (steps 4, 5) |
| Downey, *Think Stats* 2e, sec. 9 "Power", https://greenteapress.com/thinkstats2/html/thinkstats2010.html | A shuffle test inside the power loop; "if there is a difference, it is too small to detect with this sample size" (step 6 answer) |
| psyTeachR reprores v4, ch. 9, https://psyteachr.github.io/reprores-v4/09-sim.html | A coarse grid of n read off the curve rather than a search (step 4) |
| UVA Library, https://library.virginia.edu/data/articles/power-and-sample-size-analysis-using-simulation | "One big thought experiment based on our assumptions": the bold caveat (step 2) |
| Lakens, *Improving Your Statistical Inferences*, ch. 8, https://lakens.github.io/statistical_inferences/08-samplesizejustification.html; Lakens 2022 | The effect as a choice, post-hoc power adds nothing, pilot effects are imprecise, the fixed-budget stretch (steps 5-7) |
| van Belle 2008, ch. 2, Sec. 2.1 | Lehr's rule as the formula at naming (step 5) |
| Carneiro et al. 2018, S1 Data (CC BY 4.0) | Core numbers: 50% freezing, SD 17, 37% reduction, about 15 per group, typical 8-12 (steps 2-4) |
| Sipe et al. 2022 (CC0), as in notebook 3 | Transfer numbers (step 6) |
| Bakker et al. 2016, Psychol. Sci. 27:1069-1077, https://doi.org/10.1177/0956797616647519 | 89% of researchers overestimated power of small designs: the prediction in step 3 |
| Greenland et al. 2016, items 4, 8, 24-25 | "Not significant" is not "no effect" (step 3); power is not for finished studies (step 6) |
| Hoenig and Heisey 2001, Sec. 2.1 | The post-hoc power caveat (steps 6, 7) |
| Button et al. 2013, pp. 366, 369 | Median power 21%; inflation of small significant effects (step 7, stretch) |
| Gelman and Carlin 2014; Loken and Gelman 2017, Science 355:584-585, https://doi.org/10.1126/science.aal3618 | The exaggeration of significant small experiments, without the name "Type M" (stretch) |
| ARRIVE 2.0, Percie du Sert et al. 2020, https://doi.org/10.1371/journal.pbio.3000410, item 2b; E&E item 2 | "Explain how the sample size was decided"; pilots rarely give a usable spread (steps 5, 6) |
| NC3Rs EDA; Festing and Altman 2002, ILAR J. 43:244-258, "Experiment Size" | The effect as the minimum biologically interesting difference; small-pilot SDs unreliable (step 5); the notebook cites the target power of 80-95% from ARRIVE 2.0 E&E instead, whose text was checked |
| Bishop, Thompson and Parker 2022, R. Soc. Open Sci. 9:211028, https://doi.org/10.1098/rsos.211028 | Simulation alone did not transfer; state the lesson in a plain sentence after it (steps 5, 7) |
| Magnusson, https://rpsychologist.com/d3/nhst/ | With no effect, the test accuses at rate alpha; there is no power to speak of (step 5 check) |
| Hyungju Jeon, `design/05-errors-and-power.md` | Power is a curve, not one number (step 5) |

## Rejected

| Source | What | Why |
|---|---|---|
| Last year's activity 3, `plot_power_anatomy` | One tail shaded and labelled alpha | It is alpha/2; the other tail is ignored in the power too |
| Last year's activity 3 | `np.random.seed(42)`; seaborn, plotly, ipywidgets; emoji headings | One seeded `rng`; matplotlib only |
| Last year's activity 3 | A t critical value with normal power; `int((1.96 + 0.84)**2 ...)` for n | Inconsistent; `int` rounds the required n down |
| Last year's activity 3 | The four-panel power figure (curves by effect, by noise, contour, bar chart) | A dashboard; two knobs at once |
| Last year's activity 3 | "Small/medium/large" effect sizes in SD units; cancer survival as a t-test with "low noise" | Cohen's d is unmet; survival needs a different model |
| Last year's activity 3 | Fill-in strings ("what_is_alpha = ...") | A read-along, not a computation |
| Magnusson; Aberson et al. 2002, JSE 10(3) | Sliders and a solve-for panel; a four-knob applet | A dashboard |
| Magnusson; Oxford 2.4.9; Lakens ch. 2 | Two overlaid sampling distributions with a cutoff (approach B) | Assumes a known SD: at n = 5, d = 1 it gives 0.47 against 0.41 for the shuffle test; the cutoff must be recomputed for each n |
| Simon ch. 24, "Step-wise sample-size determination", pp. 405-406 | Sample until the split looks decisive | Optional stopping inflates false positives (Simon's own endnote 2 warns) |
| Simon Ex. 24-3, 24-4; *Resampling with* ch. 30 | A bootstrap null; a cutoff near p = 0.08 | Not the shuffle test students learned; alpha is 0.05 |
| *Think Stats* 2e sec. 9 | Simulating from the observed groups | Post-hoc power (rigor point 4) |
| PH525 | The t-test inside the loop | t-tests are not on this course's path; the shuffle test is |
| Lakens ch. 1 | The histogram of p-values, "first bar = power" | A second object to read; one plot form only |
| Oxford 2.4.6, 2.4.8 | A null run printing 0.1046 accepted as "about 0.05"; power at the observed effect; global `np.random` | The null check exists to catch exactly that; post-hoc power; global seed |
| Poldrack, statsthinking21 Python ch. 9; Bruce and Bruce code | `statsmodels` `solve_power` on the core path; Cohen's h fed to `TTestIndPower` | A black box needing the t-test; a wrong pairing. Named in step 7 only |
| Duke STA-663 | `while power < 0.8: n += 1` | Stops at the first noisy crossing; biases n low |
| djmannion, Programming for Psychology | Power as an image over n and effect | Two knobs at once; global `np.random` |
| Data 8 sec. 11.4; Seeing Theory | (nothing on power) | - |
| Machado slides, `old_ref/Day4 activity/` (slides 65-66) | Glucose 280 +/- 50 mg/dL, difference 100, n = 6 | The SD comes from a different experiment than the one described; d = 2 is unusually large |
| Resampling the five obese control volumes (checked 2026-10-07) | A nonparametric population for the core | Power is not monotone in n (a 12% effect: 0.32 at n = 5, 0.20 at n = 10): four clustered tumors and one outlier |
| A normal model of raw tumor volume with the drug halving it | The obese mice as the core | 14% of halved tumors fall below zero |
| Log2 tumor volume as the core measurement | Continuity with notebook 3 | A second new concept, and with the five-mouse SD, five mice already detect a halving about 70% of the time, which blurs the lesson |
| Tversky and Kahneman 1971, Psychol. Bull. 76:105-110 | "Repeat a significant experiment: will it be significant again?" | Good, but a third prediction over budget; candidate for notebook 8 or the lecture |
| Gelman and Carlin 2014 | Type S errors | Visible only at very low power |
| Festing and Altman 2002 | The resource equation | Needs ANOVA degrees of freedom |
| Horrigan et al. 2017, eLife 6:e18173 | Anti-CD47 replication planned from the original's effect | Licence of the per-animal data not checked; a lesson about pilots for later |

Not opened, so not used: the Rossman/Chance power applet (certificate error), Krzywinski and Altman (paywall),
G*Power's teaching materials, DataCamp, OpenIntro IMS sec. 14.4, the faux documentation,
Ioannidis 2005/2008, delMas, Garfield and Chance 1999 (seen only through Garfield 2002).

## Deferred to notebook 8 (experimental design)

- The experimental unit and pseudoreplication (ARRIVE 2.0 item 1; last year's activity 2).
  Notebook 6 already shows the false-positive rate of counting readings as mice (about 47%);
  notebook 8 should build on it, not repeat it.
- Randomization, blinding, and the protocol for approval (Machado slides, ARRIVE 2.0).
- Tversky and Kahneman's replication question, if not used in the lecture.

## Decisions

Each has a recommended default; the alternative follows.

1. **Number 07**, with experimental design as 08:
   Memming asked for 06 and 07 assuming two Day 2 afternoon notebooks,
   then had all three of Hyungju's merged (04-06) and asked to renumber, 2026-10-07.
2. **Fear conditioning with Carneiro et al.'s field-typical numbers as the core**, normal model
   (not: notebook 3's obese tumors in log2, or a unitless measurement; see Rejected).
3. **Two-sided test**, as published sample sizes, the worksheet, and notebooks 4-6 assume
   (not: one-sided, as notebook 3's core count).
4. **Notebook 3's plain fraction, 1000 shuffles per test** (not: the add-one p-value; rigor point 2).
5. **The null check as an optional collapsed step in naming**, since notebook 6 already ran one
   (not: its own prediction before the effect, in the Oxford order, which goes over the active-moment budget).
6. **The formal definition at naming (step 5)**, after students have computed the fraction
   (not: at the top, before the simulation).
7. **The obese transfer at 300 mm^3**, near notebook 3's observed 295, with the post-hoc caveat in the answer
   (not: a quarter reduction, 600 mm^3, about 64 per group, but 6% negative volumes).
8. **"Half the effect, four times the mice" in prose with Lehr's rule**, and in the transfer
   (not: its own tweak step in the core, over budget).
9. **500 simulated experiments per point of the curve**, to keep Colab under about half a minute
   (not: 1000, steadier by 0.006 but twice as slow).

## Found while implementing

- **Ties in decimals.** Simulated freezing values are decimals, so a shuffle that reproduces the real split
  (2 of the 252 splits at n = 5) can land a hair below `abs(observed)` and be missed,
  biasing p low near 0.05 (notebook 3's floating-point finding).
  `shuffle_test` compares against `abs(observed) - 1e-9`, as notebook 3's "Why whole numbers?" note prescribes,
  with a comment pointing there.
  With it, the no-effect rate is 0.051 at n = 5 (4000 experiments); the design-stage run without it gave 0.058.
- **A wrong DOI from the survey.** The survey gave 10.1126/science.aam5409 for Loken and Gelman (2017);
  it is Xiao and Ha (2017), "Flipping nanoscopy on its head".
  The right DOI is 10.1126/science.aal3618 (Crossref, 2026-10-07).
  Every other DOI in this note was resolved on Crossref to the intended paper.
- **Printing.** A list of numpy floats prints as `np.float64(...)` in numpy 2,
  so each sweep converts `powers` to an array and prints it rounded to two decimals.
- **Citations.** Student-facing citations are APA 7, in the text and in a References cell.
  Non-ASCII letters in author names are HTML entities (`Munaf&ograve;`, `W&uuml;rbel`),
  so the source stays ASCII and Colab renders the names correctly.
  The notebook cites the target power and the sample-size explanation from ARRIVE 2.0's
  Explanation and Elaboration, whose text was checked; Festing and Altman (2002) were seen only as an abstract page.

## Checks

2026-10-07, executed outside the repo as `colab.md` describes (`MPLBACKEND` unset):
the notebook as shipped stops at the first prediction gate with its message;
a copy with both predictions chosen, the `power` line filled, and both stretch answers appended runs clean,
in 22 s locally (Colab not measured).
With seed 20261007: lean mice p = 0.014 (exact 4/252 = 0.016); power at n = 5 0.334;
the sweep 0.36 / 0.68 / 0.85 / 0.92 / 0.99 at n = 5 / 10 / 15 / 20 / 30;
the obese sweep 0.21 / 0.42 / 0.73 / 0.93 at n = 50 / 100 / 200 / 300;
winner's curse 29.4 at n = 5; fixed budget 0.23 / 0.49 / 0.70 / 0.87 at drug means 40 / 35 / 30 / 25.
Both plots inspected: legible, one idea each.
The `.py` and `.ipynb` are synced, and both files are ASCII.
Pending: the signed-in Colab check from `colab.md`, which needs the notebook on `main`.

## References

APA 7. Paperpile status as of 2026-10-07: Greenland et al. (2016) and Simon (1997) are in the library
(`Greenland2016-fh`, `Simon1997-gh`); every other entry with a DOI was requested from the ops librarian
on 2026-10-07 (queue items from `agent-stats-and-prob-lecture`), and its metadata here is from Crossref.

Albers, C., & Lakens, D. (2018). When power analyses based on pilot data are biased: Inaccurate effect size estimators and follow-up bias. *Journal of Experimental Social Psychology, 74*, 187-195. https://doi.org/10.1016/j.jesp.2017.09.004

Bakker, M., Hartgerink, C. H. J., Wicherts, J. M., & van der Maas, H. L. J. (2016). Researchers' intuitions about power in psychological research. *Psychological Science, 27*(8), 1069-1077. https://doi.org/10.1177/0956797616647519

Bishop, D. V. M., Thompson, J., & Parker, A. J. (2022). Can we shift belief in the 'Law of Small Numbers'? *Royal Society Open Science, 9*(3), Article 211028. https://doi.org/10.1098/rsos.211028

Button, K. S., Ioannidis, J. P. A., Mokrysz, C., Nosek, B. A., Flint, J., Robinson, E. S. J., & Munaf&ograve;, M. R. (2013). Power failure: Why small sample size undermines the reliability of neuroscience. *Nature Reviews Neuroscience, 14*(5), 365-376. https://doi.org/10.1038/nrn3475

Carneiro, C. F. D., Moulin, T. C., Macleod, M. R., & Amaral, O. B. (2018). Effect size and statistical power in the rodent fear conditioning literature - A systematic review. *PLOS ONE, 13*(4), e0196258. https://doi.org/10.1371/journal.pone.0196258

Festing, M. F. W., & Altman, D. G. (2002). Guidelines for the design and statistical analysis of experiments using laboratory animals. *ILAR Journal, 43*(4), 244-258. https://doi.org/10.1093/ilar.43.4.244

Gelman, A., & Carlin, J. (2014). Beyond power calculations: Assessing Type S (sign) and Type M (magnitude) errors. *Perspectives on Psychological Science, 9*(6), 641-651. https://doi.org/10.1177/1745691614551642

Greenland, S., Senn, S. J., Rothman, K. J., Carlin, J. B., Poole, C., Goodman, S. N., & Altman, D. G. (2016). Statistical tests, P values, confidence intervals, and power: A guide to misinterpretations. *European Journal of Epidemiology, 31*(4), 337-350. https://doi.org/10.1007/s10654-016-0149-3

Hoenig, J. M., & Heisey, D. M. (2001). The abuse of power: The pervasive fallacy of power calculations for data analysis. *The American Statistician, 55*(1), 19-24. https://doi.org/10.1198/000313001300339897

Lakens, D. (2022). Sample size justification. *Collabra: Psychology, 8*(1), Article 33267. https://doi.org/10.1525/collabra.33267

Loken, E., & Gelman, A. (2017). Measurement error and the replication crisis. *Science, 355*(6325), 584-585. https://doi.org/10.1126/science.aal3618

Percie du Sert, N., Ahluwalia, A., Alam, S., Avey, M. T., Baker, M., Browne, W. J., Clark, A., Cuthill, I. C., Dirnagl, U., Emerson, M., Garner, P., Holgate, S. T., Howells, D. W., Hurst, V., Karp, N. A., Lazic, S. E., Lidster, K., MacCallum, C. J., Macleod, M., ... W&uuml;rbel, H. (2020). Reporting animal research: Explanation and elaboration for the ARRIVE guidelines 2.0. *PLOS Biology, 18*(7), e3000411. https://doi.org/10.1371/journal.pbio.3000411

Percie du Sert, N., Hurst, V., Ahluwalia, A., Alam, S., Avey, M. T., Baker, M., Browne, W. J., Clark, A., Cuthill, I. C., Dirnagl, U., Emerson, M., Garner, P., Holgate, S. T., Howells, D. W., Karp, N. A., Lazic, S. E., Lidster, K., MacCallum, C. J., Macleod, M., ... W&uuml;rbel, H. (2020). The ARRIVE guidelines 2.0: Updated guidelines for reporting animal research. *PLOS Biology, 18*(7), e3000410. https://doi.org/10.1371/journal.pbio.3000410

Simon, J. L. (1997). *Resampling: The new statistics*. Resampling Stats.

Simon, J. L., & Brett, M. (n.d.). *Resampling with: Python edition*. Retrieved October 7, 2026, from https://resampling-stats.github.io/latest-python/

Sipe, L. M., Chaib, M., Korba, E. B., Jo, H., Lovely, M. C., Counts, B. R., Tanveer, U., Holt, J. R., Clements, J. C., John, N. A., Daria, D., Marion, T. N., Bohm, M. S., Sekhri, R., Pingili, A. K., Teng, B., Carson, J. A., Hayes, D. N., Davis, M. J., ... Makowski, L. (2022). Response to immune checkpoint blockade improved in pre-clinical model of breast cancer after bariatric surgery. *eLife, 11*, e79143. https://doi.org/10.7554/eLife.79143

van Belle, G. (2008). *Statistical rules of thumb* (2nd ed.). Wiley. https://doi.org/10.1002/9780470377963
