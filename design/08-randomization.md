# Notebook 8: randomization, blinding, and the design for approval - design

Status: approved 2026-10-07 with the decisions below (decision 3: two experiments, "yes"). Implemented in `notebooks/08_randomization.py`, paired with `.ipynb` for Colab.
Ported from last year's Day 4 activity 2 (`old_ref/Day4 activity/Day4_activity2_experimental_design_v1.1.ipynb`)
and Ana Machado's slides "Steps in designing a randomised controlled animal experiment" (same folder),
redesigned rather than translated (see Rejected).
Scope set by Memming on 2026-10-07:
randomization as the one concept (chosen over blocking, the cage-level unit, or a protocol alone);
blinding and the approval protocol also in, because students will go through the Champalimaud approval process;
the protocol written in the language of Ana's slide "9 - Reporting a design experiment",
with our own sentences and credit to her (the repo is public; nothing from `old_ref/` is published);
the exact Champalimaud SOPs are not checked.
Built from a prior-art survey (`AGENTS.md`, "Starting a new notebook"):
`old_ref/` and its books, interactive tools, Python notebooks, courses, GitHub,
misconception research, methods and meta-research on animal experiments, and published data.

## Where it sits

Day 3 morning, second, after notebook 7 (power); the last notebook of the series so far.
Students arrive with the shuffle test (notebook 3), the Type I error rate as the fraction of experiments
that reject when the drug does nothing (notebooks 5-7; notebook 7's optional "null check"),
and notebook 6's lesson that one mouse is one observation.
Notebook 7 planned how many mice; this notebook plans who gets the drug and who knows it,
then writes the plan down for approval.

It serves the `README.md` objectives
"Design an experiment's sample size and write a practical protocol for approval" (with notebook 7)
and "Develop, formulate, execute, and interpret statistical tests of biological hypotheses".

## Final observation

"Assigning the drug at random keeps a hidden difference between mice from posing as a drug effect."

Blinding is the transfer: the same check shows a second hidden difference, in how the mice are scored,
which randomization does not remove.

## Python practice

`rng.permutation` of a list of group labels, as the random assignment itself,
and selecting a group's values with a comparison (`temperature[group == "drug"]`, notebook 1's `rolls == 3` and notebook 5's `heads[caught]`).
The last section turns the same line into a randomisation sheet for a real experiment.

## Data and simulation parameters

**Core: the order mice are taken out of the cage.**
Takao, Shoji, Hattori and Miyakawa (2016), Front. Behav. Neurosci. 10:99, https://doi.org/10.3389/fnbeh.2016.00099:
in group-housed C57BL/6J mice removed one after another from the home cage,
"Rectal temperature increased in a stepwise manner according to the position of sequential removal",
F(4, 1695) = 52.29; body weight was not affected (F(4, 1695) = 2.29).
The mice left waiting are disturbed by the removals.
Means read from their Figure 1 (I read the figure; bars are SEMs):
36.1, 36.45, 36.7, 36.8, 37.15 C at positions 1-5 (n = 445, 440, 412, 363, 40).
The within-position SD, derived from the reported F and these means, is 0.81 C.
Positions 1 vs 4: 0.86 SD; the first two vs the last two of a cage of four: 0.58 SD (0.47 C).
The same paper reports removal-order effects on corticosterone, hot-plate latency, and the elevated plus maze.

The notebook simulates cages of four with temperature = the position mean + normal(0, 0.8) per mouse,
**a drug that does nothing**, and two allocations:
"first two caught in each cage get the drug" (convenience) and `rng.permutation` of the same labels (random).
**The simulation is handed the catch-order effect and knows the drug does nothing; the notebook says both in bold.**

Computed 2026-10-07, seed 20261007, 1000 simulated experiments per row,
notebook 7's `shuffle_test` (two-sided, 1000 shuffles, ties counted with `- 1e-9`):

| Cages of 4 (mice per group) | False positives, first two caught | False positives, random | Drug minus control, mean (SD), first caught | random |
|---|---|---|---|---|
| 3 (6 vs 6) | 0.133 | 0.051 | -0.46 C (0.46) | +0.00 (0.50) |
| 5 (10 vs 10) | 0.229 | 0.048 | -0.45 C (0.36) | -0.01 (0.38) |
| 10 (20 vs 20) | 0.454 | 0.055 | -0.48 C (0.24) | -0.00 (0.27) |

More mice make convenience allocation worse, not better: the offset stays, the noise shrinks.

**Transfer: an observer who knows the groups.**
Freezing scored by eye (notebook 7's measurement: 50%, SD 17), groups randomized, a drug that does nothing,
and an unblinded scorer who shades each drug-treated mouse 4 points lower: 0.23 SD,
the pooled amount by which nonblinded assessors made treatments look better
than blinded assessors of the same patients, in 16 randomized trials with subjective measurement scales
(Hrobjartsson et al., 2013, CMAJ 185:E201-E211, https://doi.org/10.1503/cmaj.120744).
**Borrowed from human trials; the notebook says so in bold.**
Holman et al. (2015), PLOS Biology, https://doi.org/10.1371/journal.pbio.1002190,
found the same direction across the life sciences: nonblind studies report larger effects and more significant p-values.

| Mice per group | False positives, scorer blind | scorer shading by 4 points |
|---|---|---|
| 10 | 0.044 | 0.077 |
| 20 | 0.064 | 0.123 |
| 40 | 0.049 | 0.179 |

(1000 experiments each; Monte Carlo SD about 0.007 near 0.05.)

**Stretch: the drug in the drinking water.**
Whole cages are treated, so the cage is the unit and cages must be randomized and shuffled.
Simulated by the survey (cages of 5, cage share of variance 0.1-0.4, within the published range:
Varholick et al. 2019, Sci. Rep., https://doi.org/10.1038/s41598-019-49612-0, 0-0.46 for behavior and stress hormones):
shuffling mice gives 9-28% false positives; shuffling cages holds 5%,
but needs at least 4 cages per arm (with 3, the smallest two-sided p is 0.10, so the test can never reject).
A real case: Russell et al. (2022), Cell Reports, https://doi.org/10.1016/j.celrep.2022.110783,
gave an antibiotic in the drinking water to 12 mice per group housed as 3 cages of 4 or 6 cages of 2.

## Rigor: what the notebook states, and the sources

1. **Random assignment makes the shuffle test exact for any hidden factor.**
   If the drug does nothing, each mouse's value is what it would have been under either label;
   the only random thing is which labels the mice got, so shuffling the labels re-runs the assignment
   and P(p <= alpha) <= alpha, whatever the mice differ by
   (Ernst, 2004, Sec. 3, p. 677: "The sole basis for inference in the randomization model is the random assignment
   of available subjects to treatment groups"; inferences "are limited to the subjects in the study").
   Fisher (1935, Ch. II, Sec. 10, p. 24): "the simple precaution of randomisation will suffice to guarantee
   the validity of the test of significance". Seen in the 1935 first edition scan
   (https://archive.org/details/in.ernet.dli.2015.502684) by the survey.
   Called a **randomization test** when the labels were randomly assigned (OpenIntro IMS, ch. 11 footnote).
2. **Randomization balances only on average.** One random assignment can leave the groups unequal;
   the 5% of randomized experiments that reject are those draws.
   ARRIVE 2.0 E&E Box 4 (Percie du Sert, Ahluwalia, et al., 2020) goes further: simple randomisation
   "is rarely appropriate, as it cannot ensure that comparison groups are balanced for other variables",
   and it recommends randomisation within blocks (here: by cage, with a within-cage shuffle to match).
   Found while implementing (the survey had quoted only the second half); the notebook teaches complete
   randomization, which is valid, and names blocking as ARRIVE's next step, beyond this notebook.
3. **Haphazard is not random.** ARRIVE 2.0 E&E, item 4a: "Selecting an animal 'at random' (i.e., haphazardly or arbitrarily)
   from a cage is not statistically random, as the process involves human judgement",
   and "Inferential statistics based on nonrandomised group allocation are not valid."
   NC3Rs EDA, https://eda.nc3rs.org.uk/experimental-design-allocation: failing to randomise
   "increases the risk of false positive results".
4. **Random assignment is not random sampling.** Assignment licenses "the drug did it, in these mice";
   generalizing to other mice needs random sampling (Ernst, 2004, Secs. 3-4; OpenIntro IMS Fig. 2.8),
   notebook 1's sampling.
5. **Randomization does not blind.** Bias in measurement survives random assignment (the transfer);
   ARRIVE 2.0 E&E item 5 (blinding and allocation concealment).
6. **Shuffle what was randomized.** When whole cages are treated, the cage is the experimental unit,
   "also sometimes called the unit of randomisation" (ARRIVE 2.0 E&E, item 1b;
   Lazic, Clarke-Williams & Munafo, 2018: when a drug goes in the drinking water, "the cages are the EUs";
   Festing & Altman, 2002: "the analysis should reflect the way the randomization was done").
7. **How big is the problem in practice? Real but variable.** Studies not reporting randomization were more often positive
   (Bebarta et al., 2003: odds ratio 3.4, 95% CI 1.7-6.9, 290 animal-study abstracts);
   across 31 systematic reviews the average inflation was small, SMD 0.07 (0.02-0.12), larger outside stroke
   (Hirst et al., 2014); in stroke Crossley et al. (2008) found no significant effect.
   Reported randomization is rare: 12% of 271 studies (Kilkenny et al., 2009); 20% of 134 (Macleod et al., 2015).
   The notebook says "more often", not "always", and makes no size claim beyond its own simulation.

## Step ladder

About 15-20 minutes for steps 1-7, plus about 10 minutes of writing in step 8.
At most one new thing per step.
A setup cell creates `rng = np.random.default_rng(20261007)` and repeats notebook 7's `shuffle_test` (unchanged, said so).

1. **Mice taken out later are warmer.**
   The plan: test whether a drug lowers body temperature, measured with a rectal thermometer.
   Takao et al. (2016): in a cage of four, the mouse taken out first is about 36.1 C, the fourth about 36.8 C,
   because the mice left behind are disturbed.
   `np.tile([36.1, 36.45, 36.7, 36.8], 5)` printed raw: five cages of four, in catch order.
   One simulated set of 20 temperatures: that plus `rng.normal(0, 0.8, size=20)`.
   Bold: here we play nature; the simulation knows the catch order matters and that the drug does nothing.
   New: `np.tile`.
2. **First caught, first treated.**
   The convenient allocation: the first two mice caught in each cage get the drug.
   `group = np.tile(["drug", "drug", "control", "control"], 5)` printed raw,
   then `shuffle_test(temperature[group == "control"], temperature[group == "drug"])` on one experiment.
   New: selecting by a comparison on a label array.
3. **Predict, then 1000 experiments.**
   Dropdown with the gate: "The drug does nothing. How often will the test 'detect' it?"
   (about 5%, as in notebook 7 / about 20% / about 50% / almost always).
   The loop keeps each p-value and each estimated effect (drug minus control).
   Print the fraction with p <= 0.05; histogram of the estimated effects with a line at 0.
   Collapsed answer: about 23%; the histogram centers near -0.45 C, not 0:
   the "drug" group is cooler before any drug, because it holds the first-caught mice.
   The test is not fooled: the groups really differ. Crediting the drug is the mistake.
   Active: predict. Plot 1.
4. **Shuffle the labels before the experiment.**
   Students fill one line: `group = ...` with `rng.permutation(group)`, the random assignment,
   in a copy of step 3's loop. Print the fraction and the histogram.
   Collapsed answer: about 5%, centered on 0.
   Prose asks: print one experiment's mean catch position per group (bold: no lab sees this).
   Is it equal? No: one random assignment is never exactly balanced; on average it is (rigor point 2).
   Active: fill one line. Plot 2.
5. **More mice do not fix it.**
   One cell runs both allocations with `cages = 5` and prints both false-positive rates.
   Tweak: `cages = 10`. Predict in prose first.
   Collapsed answer: first-caught rises to about 45%; random stays about 5%.
   More mice shrink the noise, not the offset (delMas & Fry's "Strength Shoe" question; markthalle's "noise, not bias").
   Active: tweak and observe.
6. **Name it.**
   The student says what the simulation showed (collapsed answer).
   Names: a **confounder** or bias (a difference between the groups other than the drug);
   **randomization** (random assignment); the **randomization test** (the shuffle test re-running the assignment).
   Rigor points 1-4 in plain words, with Fisher's sentence and ARRIVE's "haphazard is not random".
7. **Worked transfer: who scores the mice?**
   Freezing scored by eye, groups randomized, the drug does nothing.
   An observer who knows the groups shades each drug-treated mouse 4 points lower (bold: size borrowed from human trials).
   Dropdown: "Randomized groups, an observer who knows them. False positives?" (about 5% / more than 5%).
   One cell: 1000 experiments of 20 per group, scored blind and scored knowing the groups.
   Collapsed answer: about 5% blind, about 12% knowing; with 40 per group about 18%.
   Randomization keeps hidden differences out of who gets the drug; blinding keeps them out of how it is measured.
   **Blinding**: whoever gives the treatment and whoever measures do not know which group a mouse is in;
   a third party holds the code.
   Active: predict.
8. **Write it down: the design for approval.**
   One code cell makes a randomisation sheet:
   mouse IDs `M01`-`M12`, labels `rng.permutation(["A"] * 6 + ["B"] * 6)`, printed as a table;
   the key (which letter is the drug) stays with a third party.
   Then the design paragraph, with little effort and no blank page (Memming, 2026-10-07:
   "writing part must be not too much effort and pleasant UX"):
   one Colab form cell, pre-filled with the worked example (the temperature experiment of steps 1-5),
   with short text fields (question, drug and dose, outcome measure),
   dropdowns (experimental unit: individual animal / cage / litter / part of the animal;
   who prepares the coded doses; who measures blind), and number fields
   (difference worth finding, SD, power, and the n from notebook 7).
   Running the next cell prints the finished paragraph in the order and vocabulary of
   Ana Machado's slide "9 - Reporting a design experiment", with our own sentences:
   the hypothesis and the experiment; the experimental unit (an animal that "can be allocated independently");
   allocation by a randomisation spreadsheet; allocation concealed by a third party who prepares coded doses;
   the outcome measure, measured blind; the independent variable and its categories;
   the analysis, carried out blind on groups "A" and "B"; and the sample size, with its inputs.
   Students change a few fields to describe their own experiment, rerun, and copy the paragraph.
   The worked example uses one consistent experiment (fixing the slide's mismatch, see Rejected).
   A form earns its place here (`demo-design.md`, "Edit a literal before reaching for a widget"):
   this step is a writing aid, not a statistical concept, and the fields are many.
   Pointers: ARRIVE 2.0 Essential 10 (https://arriveguidelines.org), the NC3Rs EDA,
   and "the Champalimaud Vivarium SOPs and the ORBEA process (see Ana Machado's slides)" without the internal URL.
   Not counted as an active moment; it is a writing exercise.
9. **You can now ...**
   assign treatments at random, blind the people who treat and measure,
   and write the design so that an approval committee can check it.
   Closing: "Student" (1931), the Lanarkshire milk experiment: teachers replaced randomly chosen children
   "to obtain a more level selection", and the comparison was spoiled;
   Cobb (2007)'s question: "Where was the randomization, and what inferences does it support?"
   Last, in one plain sentence: "Let chance decide who gets the drug, so that nothing else can."

**Stretch (optional):**
- **The drug in the drinking water.** Cages of 5, cages randomized; shuffle mice vs shuffle cage means;
  then try 3 cages per arm and see that the cage-level test can never reach 0.05 (only 20 relabelings).
- **Which randomized experiments reject?** Under random assignment, keep the gap in mean catch position;
  the experiments with p <= 0.05 are the unlucky draws (rigor point 2).

Budget: 9 steps, 4 active moments (3, 4, 5, 7), two plots (steps 3 and 4), plus a writing exercise.
This is at the top of `demo-design.md`'s budget; see decision 2.

Python constructs met, in order:
`np.tile`, `rng.normal(..., size=20)`, a comparison selecting values (`temperature[group == "drug"]`),
the loop of notebook 7, `plt.hist` with `plt.axvline` (notebook 3), `rng.permutation` on labels,
`["A"] * 6 + ["B"] * 6`, printing a table with a `for` loop.
Deliberately absent: pandas, `.ravel`, 2-D arrays, blocking, ANOVA, any widget.

## Visualization

Two histograms of the same form: the estimated drug effect (drug minus control, C) over 1000 simulated experiments,
with a vertical line at 0, the true effect.
Convenience allocation centers near -0.45 C; random assignment centers on 0.
Same x-range in both, so the shift is seen directly.
No plot of the hidden factor's balance (prose and one printed number instead), no multi-covariate display.

## Adopted

| Source | What we took |
|---|---|
| Takao et al. 2016, https://doi.org/10.3389/fnbeh.2016.00099 | The hidden factor and its size (steps 1-5) |
| Rossman/Chance "Randomizing Subjects" applet, http://www.rossmanchance.com/applets/Subjects.html | Reveal the hidden factor after allocation, in bold as unseen by a real lab (step 4) |
| delMas & Fry, "Random is Random", http://mathquest.carroll.edu/activestats/ConferenceMaterials/Random-is-Random-delMas-Fry.pdf | "Similar but not identical" groups; walk-in-order allocation as the misconception (steps 3-5) |
| marinelavoda/markthalle-randomization-sim (GitHub) | Histogram of the estimated effect off-center vs centered; "more data reduces noise but not bias" (steps 3-5) |
| scottminkoff/randomsim (GitHub) | "Doesn't guarantee perfect balance, but differences are due to chance alone" (step 6) |
| Data 8 ch. 12.1-12.2, https://inferentialthinking.com | Same shuffle, different licence: association vs causation (step 6) |
| OpenIntro IMS, Fig. 2.8 and ch. 11 | Sampling licenses generalization, assignment causation; "randomization test" (step 6) |
| randomizr / ri2 vignettes (DeclareDesign) | Complete random assignment with fixed group sizes: `rng.permutation` of labels (step 4) |
| Mixtape ch. 4, https://mixtape.scunning.com/04-potential_outcomes_and_randomization | The shuffle "should reflect the way the data was initially assigned" (stretch) |
| CASRAI pseudoreplication guide | "Could these two have gone into different groups?" (stretch) |
| Stat 20, Berkeley | Balance "on average" (step 6) |
| Fisher 1935 | The validity sentence (step 6, rigor 1) |
| Ernst 2004 | The randomization model, inference limited to these subjects (rigor 1, 4) |
| ARRIVE 2.0 E&E items 1b, 4a, 5, Box 4 | Haphazard is not random; balance not guaranteed; unit of randomisation; blinding (steps 6-8) |
| NC3Rs EDA allocation page | "Increases the risk of false positive results" (step 6) |
| Ana Machado's slides (old_ref, not published) | The order and vocabulary of the design write-up; drinking water means the cage is the unit; blinding by a third party with coded doses (steps 7-8, stretch) |
| Hrobjartsson et al. 2013; Holman et al. 2015 | The size and direction of observer bias (step 7) |
| delMas, Garfield, Ooms & Chance 2007, SERJ, https://doi.org/10.52041/serj.v6i2.483 | Random assignment confused with random sampling grew from 36% to 49% after a course (step 6, rigor 4) |
| Kaplan, Rogness & Fisher 2014, SERJ, https://doi.org/10.52041/serj.v13i1.296 | Random is a property of the procedure, not of how the groups look (step 6) |
| Reinhart et al. 2022, JSDSE, https://doi.org/10.1080/26939169.2022.2063209 | Students cite confounders even after randomization: the step 4 balance question |
| Chance et al. 2024, JSDSE, https://doi.org/10.1080/26939169.2024.2333736 | Shuffling models random assignment (rigor 1) |
| Cobb 2007, TISE, https://doi.org/10.5070/t511000028 | The closing question (step 9) |
| "Student" 1931, Biometrika, https://doi.org/10.2307/2332424 | The closing anecdote (step 9) |
| Lazic, Clarke-Williams & Munafo 2018; Festing & Altman 2002 | The cage as the unit; analyse as randomized (stretch, rigor 6) |
| Bebarta 2003; Hirst 2014; Crossley 2008; Kilkenny 2009; Macleod 2015 | Real-world size and prevalence, stated with their variability (rigor 7, step 9) |

## Rejected

| Source | What | Why |
|---|---|---|
| Last year's activity 2 | Fill-in strings for unit, sample size, hypotheses; four scenarios; multi-panel decorative figures; `np.random.seed(42)`, plotly, emoji | A read-along; scenario 1.1's plot itself puts participants 1-30 on the drug (convenience allocation) |
| Machado slides | Randomization filed under "Minimize inter-individual variability" | Randomization removes bias; it does not reduce variance |
| Machado slide 9 | "Plasma biomarker in normal mice" with the SD of glucose in diabetic mice | One consistent experiment in our worked example |
| Rossman/Chance applet | Three covariates at once; the block toggle | One idea per plot; blocking is a second concept |
| elinw/randomization | Class-pooled spreadsheets, coin-flip assignment | Students work alone; coin flips vary group sizes |
| markthalle sim; NoraZitnick/stat-sim | Selection-strength slider and presets | A dashboard |
| Data 8 ch. 12.2; Mixtape | "Ensures that there is no confounding variable"; "physical randomization is balancing everything" | Balance holds only on average (rigor 2) |
| Mixtape | Potential-outcomes notation; "first 50,000 patients" as if random | Notation unmet; first-N is exactly what the notebook shows failing |
| Stat 20 | A test of covariate balance after randomization | Its null is true by design |
| Sawilowsky 2004, JMASM, https://doi.org/10.22237/jmasm/1083370980 | Non-significant baseline tests as proof of equal groups | Absence of evidence; teaches baseline testing |
| Falk & Konold 1997, Psych. Rev. | Humans generating random sequences | Students never allocate by hand here |
| Lady tasting tea | As a step | A new story; Fisher's sentence carries the point |
| Simon, *Resampling* ch. 18, 23; *Resampling with* | Random assignment as a design principle | Essentially absent; the mouse shuffle is justified by a common universe, not allocation |
| Blocking (Machado slides; OpenIntro Fig. 2.6) | Randomized block design | A second concept; candidate for a later notebook |
| A blanket "nonrandomized studies show larger effects" | - | Crossley 2008 found none in stroke; Hirst 2014's average is small |
| Trevarthen et al. 2025, R. Soc. Open Sci., https://doi.org/10.1098/rsos.251069 (CC0, cage IDs) | Real cage-level data for the stretch | Only 2 mice per cage, so shuffling mice inflates the result only mildly; the simulation shows the point plainly |
| The Champalimaud SOP folder (Ana's slide 8) | Matching the protocol to the exact SOPs | Not checked, per Memming; the notebook points to it in words, not by its internal URL |

Not opened, so not used: Lock5, Downey on random assignment, ISCAM instructor notes, Landes 2024,
Aarts et al. and Holson & Pearce (seen only as quoted), Derry et al. 2000, Wagler & Wagler 2014,
Senn 2013 "Seven myths of randomisation".

## Decisions

Each has a recommended default; the alternative follows.
Memming, 2026-10-07: decision 2 ok, with a low-effort writing step (step 8 is a form);
decisions 5 and 6 ok; references to Paperpile with the `teaching` label, yes;
decision 3 asked "that's a different experiment?"; after the answer below, two experiments, "yes".

1. **Name `notebooks/08_randomization.py`**, under the `README.md` heading "Experimental design"
   (not: `08_design.py`).
2. **Randomization, blinding, and the protocol in one notebook**, about 15-20 minutes of computing plus 10 of writing,
   at the top of the budget (not: the protocol as a separate paper worksheet, like the coin worksheet,
   which would keep the notebook at 15 minutes and give the protocol its own build).
3. **Two experiments, said plainly: rectal temperature in the core, the fear-memory test in the transfer.**
   The catch-order effect is measured on temperature (Takao et al., 2016), an objective measurement;
   the observer-bias size (0.23 SD) comes from subjective rating scales, and Holman et al. (2015) find bias strongest
   for subjective variables, so the transfer uses notebook 7's freezing scored by eye,
   introduced as "the same lab's next experiment".
   Alternatives: one experiment throughout, either freezing (the catch-order effect on freezing would be invented)
   or temperature (the blinding bias would have no sourced size).
4. **Convenience allocation as "the first two caught in each cage"**, the ARRIVE and NC3Rs example
   (not: "cage 1 gets the drug, cage 2 control", which mixes in the cage-as-unit lesson).
5. **The cage-in-drinking-water lesson as a stretch** (not: the transfer, replacing blinding).
6. **The protocol pointer names the Champalimaud SOPs and ORBEA process in words**, without the internal Drive URL,
   since the repo is public (not: the URL from Ana's slide).
7. **Ana Machado credited by name** in the protocol section and the design note.

## Changes elsewhere

- `README.md`: the Colab link under "Experimental design".
- `IMPL.md`: the log.
- `~/p/memmingCommons/ai-agent/services/ops/url-allowlist.txt`: `cmaj.ca`, `projecteuclid.org`, `escholarship.org`,
  `ahajournals.org`, `iase-pub.org` (Memming, 2026-10-07), so that the librarian could add this note's references.

## Found while implementing

- **ARRIVE Box 4 in context** (rigor point 2): simple randomisation "is rarely appropriate";
  the notebook says so and names blocking as the next step.
- **Fisher's exception.** The full sentence on p. 24 begins "Apart, therefore, from the avoidable error of the experimenter
  himself introducing with his test treatments, or subsequently, other differences in treatment":
  Fisher's own statement that randomization does not cover what blinding covers. Quoted in the blinding answer.
  Checked in the archive.org text of the first edition (Section 10, "The Effectiveness of Randomisation", p. 24).
- **Student (1931) checked in the text**: 10000 children with milk, 10000 controls, spring 1930;
  substitution "in order to obtain a more level selection"; the controls "definitely superior both in weight and height
  to the 'feeders' by an amount equivalent to about 3 months' growth in weight and 4 months' growth in height";
  Student attributes it to teachers unconsciously giving the milk to the ill-nourished.
- **p printed as 0.0.** The first convenience experiment with the notebook's seed prints p = 0.0 (no shuffle of 1000 as extreme);
  the markdown after it says this means below 1/1000, never 0, as notebook 3 taught.
- **The form's third-party sentence** does not start with the field, so a name typed there keeps its capitals
  (`str.capitalize` would lowercase the rest).
- **Takao's SD.** The survey's effect sizes assumed too small an SD; derived from the reported F and the figure's means,
  the within-position SD is 0.81 C, so the first-two vs last-two gap is 0.58 SD, not about 1.

## Checks

2026-10-07, executed outside the repo as `colab.md` describes (`MPLBACKEND` unset):
the notebook as shipped stops at the first prediction gate with its message;
a copy with both predictions chosen, the random-assignment line filled, and the stretch answer appended runs clean,
in 21 s locally (Colab not measured).
With seed 20261007: first-caught allocation 0.218 with p <= 0.05 (histogram centered near -0.45 C);
random 0.054 (centered on 0); one random assignment's mean catch positions 2.6 vs 2.4;
the 5-cage comparison 0.24 vs 0.051; blinding 0.034 blind vs 0.106 knowing the groups
(0.044 vs 0.123 in the design-stage run, so the answer says "about 11%");
stretch: shuffling mice 0.151, shuffling cages 0.032; the design paragraph prints in full.
The 10-cage numbers (0.454 vs 0.055) and 40-per-group blinding (0.179) come from the design-stage runs above.
Both plots inspected: same axis, centered where the answers say.
The `.py` and `.ipynb` are synced, and both files are ASCII.
Pending: the signed-in Colab check from `colab.md` (form fields, dropdowns), which needs the notebook on `main`.

## References

APA 7. Metadata from Crossref unless stated.
Paperpile: requested from the ops librarian on 2026-10-07 with the `teaching` label (Memming's "yes");
already there from notebook 7: Festing and Altman (2002), ARRIVE 2.0 E&E.
Fisher (1935) and Machado (2024) have no DOI and are not in Paperpile.

Bebarta, V., Luyten, D., & Heard, K. (2003). Emergency medicine animal research: Does use of randomization and blinding affect the results? *Academic Emergency Medicine, 10*(6), 684-687. https://doi.org/10.1111/j.1553-2712.2003.tb00056.x

Chance, B., McGaughey, K., Chung, S., Goodman, A., Roy, S., & Tintle, N. (2024). Simulation-based inference: Random sampling vs. random assignment? What instructors should know. *Journal of Statistics and Data Science Education, 33*(1), 116-125. https://doi.org/10.1080/26939169.2024.2333736

Cobb, G. W. (2007). The introductory statistics course: A Ptolemaic curriculum? *Technology Innovations in Statistics Education, 1*(1). https://doi.org/10.5070/t511000028

Crossley, N. A., Sena, E., Goehler, J., Horn, J., van der Worp, B., Bath, P. M., Macleod, M., & Dirnagl, U. (2008). Empirical evidence of bias in the design of experimental stroke studies: A metaepidemiologic approach. *Stroke, 39*(3), 929-934. https://doi.org/10.1161/STROKEAHA.107.498725

delMas, R., Garfield, J., Ooms, A., & Chance, B. (2007). Assessing students' conceptual understanding after a first course in statistics. *Statistics Education Research Journal, 6*(2), 28-58. https://doi.org/10.52041/serj.v6i2.483

Ernst, M. D. (2004). Permutation methods: A basis for exact inference. *Statistical Science, 19*(4), 676-685. https://doi.org/10.1214/088342304000000396

Festing, M. F. W., & Altman, D. G. (2002). Guidelines for the design and statistical analysis of experiments using laboratory animals. *ILAR Journal, 43*(4), 244-258. https://doi.org/10.1093/ilar.43.4.244

Fisher, R. A. (1935). *The design of experiments*. Oliver and Boyd.

Hirst, J. A., Howick, J., Aronson, J. K., Roberts, N., Perera, R., Koshiaris, C., & Heneghan, C. (2014). The need for randomization in animal trials: An overview of systematic reviews. *PLOS ONE, 9*(6), e98856. https://doi.org/10.1371/journal.pone.0098856

Holman, L., Head, M. L., Lanfear, R., & Jennions, M. D. (2015). Evidence of experimental bias in the life sciences: Why we need blind data recording. *PLOS Biology, 13*(7), e1002190. https://doi.org/10.1371/journal.pbio.1002190

Hr&oacute;bjartsson, A., Thomsen, A. S. S., Emanuelsson, F., Tendal, B., Hilden, J., Boutron, I., Ravaud, P., & Brorson, S. (2013). Observer bias in randomized clinical trials with measurement scale outcomes: A systematic review of trials with both blinded and nonblinded assessors. *Canadian Medical Association Journal, 185*(4), E201-E211. https://doi.org/10.1503/cmaj.120744

Kaplan, J. J., Rogness, N. T., & Fisher, D. G. (2014). Exploiting lexical ambiguity to help students understand the meaning of random. *Statistics Education Research Journal, 13*(1), 9-24. https://doi.org/10.52041/serj.v13i1.296

Kilkenny, C., Parsons, N., Kadyszewski, E., Festing, M. F. W., Cuthill, I. C., Fry, D., Hutton, J., & Altman, D. G. (2009). Survey of the quality of experimental design, statistical analysis and reporting of research using animals. *PLOS ONE, 4*(11), e7824. https://doi.org/10.1371/journal.pone.0007824

Lazic, S. E., Clarke-Williams, C. J., & Munaf&ograve;, M. R. (2018). What exactly is 'N' in cell culture and animal experiments? *PLOS Biology, 16*(4), e2005282. https://doi.org/10.1371/journal.pbio.2005282

Machado, A. (2024). *Steps in designing a randomised controlled animal experiment* [Lecture slides]. Champalimaud Foundation.

Macleod, M. R., Lawson McLean, A., Kyriakopoulou, A., Serghiou, S., de Wilde, A., Sherratt, N., Hirst, T., Hemblade, R., Bahor, Z., Nunes-Fonseca, C., Potluru, A., Thomson, A., Baginskitae, J., Egan, K., Vesterinen, H., Currie, G. L., Churilov, L., Howells, D. W., & Sena, E. S. (2015). Risk of bias in reports of in vivo research: A focus for improvement. *PLOS Biology, 13*(10), e1002273. https://doi.org/10.1371/journal.pbio.1002273

Percie du Sert, N., Ahluwalia, A., Alam, S., Avey, M. T., Baker, M., Browne, W. J., Clark, A., Cuthill, I. C., Dirnagl, U., Emerson, M., Garner, P., Holgate, S. T., Howells, D. W., Hurst, V., Karp, N. A., Lazic, S. E., Lidster, K., MacCallum, C. J., Macleod, M., ... W&uuml;rbel, H. (2020). Reporting animal research: Explanation and elaboration for the ARRIVE guidelines 2.0. *PLOS Biology, 18*(7), e3000411. https://doi.org/10.1371/journal.pbio.3000411

Reinhart, A., Evans, C., Luby, A., Orellana, J., Meyer, M., Wieczorek, J., Elliott, P., Burckhardt, P., & Nugent, R. (2022). Think-aloud interviews: A tool for exploring student statistical reasoning. *Journal of Statistics and Data Science Education, 30*(2), 100-113. https://doi.org/10.1080/26939169.2022.2063209

Russell, A., Copio, J. N., Shi, Y., Kang, S., Franklin, C. L., & Ericsson, A. C. (2022). Reduced housing density improves statistical power of murine gut microbiota studies. *Cell Reports, 39*(6), 110783. https://doi.org/10.1016/j.celrep.2022.110783

Student. (1931). The Lanarkshire milk experiment. *Biometrika, 23*(3/4), 398-406. https://doi.org/10.2307/2332424

Takao, K., Shoji, H., Hattori, S., & Miyakawa, T. (2016). Cohort removal induces changes in body temperature, pain sensitivity, and anxiety-like behavior. *Frontiers in Behavioral Neuroscience, 10*, 99. https://doi.org/10.3389/fnbeh.2016.00099

Varholick, J. A., Pontiggia, A., Murphy, E., Daniele, V., Palme, R., Voelkl, B., W&uuml;rbel, H., & Bailoo, J. D. (2019). Social dominance hierarchy type and rank contribute to phenotypic variation within cages of laboratory mice. *Scientific Reports, 9*, 13650. https://doi.org/10.1038/s41598-019-49612-0

