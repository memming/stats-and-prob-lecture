# Designing a teaching demo

How to plan and review one notebook in this repo:
a computational experiment of about 15 minutes (10-20)
from which a programming novice leaves understanding one statistical concept
and having practiced one useful Python move.
Coding takes some effort, but should not consume the statistical lesson.

## Ground rules

A notebook is an exposition that happens to run, so judge it as prose.
Headings state claims ("Averages of many tosses barely move"), not topics ("Simulation").
The first cell states the takeaway in one sentence
and says where the notebook sits: what comes before, what comes after,
and whether it is core or optional.
Each cell does one step, usually in under ten lines.
Variable names mirror the symbols they stand for.
Code that *is* the concept stays visible;
plumbing such as plot styling may be hidden,
but only after the student has seen it once in the open,
and under a name that never needs opening.
When a demo is handed something a real analysis would not have -
the true standard deviation instead of its estimate, say -
state that in bold where it happens.
A student who finds the shortcut alone stops trusting the rest.

Exercises take three shapes:
**predict** ("before running, will this get more or less variable?"),
**tweak and observe** (change `N`, rerun, explain the plot),
and **fill one line**, where the single blank line is the concept itself
and the cell runs once it is filled.
Actually blank that line; a solution with the prompt trailing as a comment is a read-along.
Give students enough working code around the blank to diagnose a mistake.
Let them try before revealing the answer, but do not let a syntax error
block the rest of the statistical exercise.
Harder exercises are labeled `**Stretch (optional):**`,
and the core path alone covers every concept.
Each exercise and each prediction has a collapsed answer directly below it,
with the reasoning, not only the code:
a student alone in a browser has nobody else to check against.

## Workflow

1. **Name the final observation.**
   One sentence the student should be able to say at the end,
   in ordinary language and without referring to code:
   "the average of a few tosses jumps around; the average of many settles down."
   If stating it takes an "and", it is two demos.
2. **Pick the smallest system that makes it unmistakable** -
   coins, dice, a random walk, a noisy measurement.
   Realism is not a goal here; the biological example comes at the close.
3. **Design backwards.**
   From the observation, list the experiment that makes it visible,
   the representation that shows it most plainly,
   and what the student must already understand to read that representation.
   The step ladder is that list reversed.
   Cut every step that is not on it.
4. **Build representations up.**
   An object before any summary of it, a summary before a plot of summaries:
   one draw, many draws, their mean, many means, a histogram of means.
   Every axis names something the student has already held.
5. **Place the active moments.**
   Two to four places where the student changes one value and reruns,
   most of them preceded by a one-line prediction.
   Exactly one thing changes per moment.
6. **Choose the Python practice.**
   Name the one library call or language move students will write or debug.
   For each other construct the student must read, ask whether the concept needs it.
   Functions, classes, comprehensions, fancy indexing, callbacks,
   and plotting infrastructure usually do not.
   An unavoidable new construct gets its own step,
   shown working on something trivial, before the concept depends on it.
7. **Check the budget:**
   one phenomenon, 5-9 steps, 2-4 active moments,
   at most two plots, one closing explanation.
   Over budget means cutting scope, not adding explanation or speeding up.
8. **Close in this order:**
   the student explains what they saw to an imagined classmate,
   then the conventional name, then the formula if there is one,
   then "you can now..." with a transfer to a measurement
   from cancer immunology or neuroscience.

## Rules

- **At most one new thing per step** among a concept, a Python construct,
  a kind of plot, and an interaction mechanism.
- **Show a function's raw output before composing it.**
  Any call students may not know is first run alone, with its output shown:
  `rolls == 3` before `(rolls == 3).sum()`, `np.arange(0.5, 7)` before it becomes bin edges.
  This is not the lesson; it removes friction
  and models the habit of looking at what a call returns.
- **Knobs arrive one at a time, where they are used.**
  The notebook unfolds as a sequence, never as a dashboard:
  no control panel at the top, and at most one new knob per step,
  placed beside the output it changes.
  Each step owns its controls;
  a control read by two steps couples them,
  and the step that was not rerun keeps showing the old value.
- **Prose asks; it does not pre-explain.**
  "Run this again. Same answer?" comes before any paragraph about variability.
  Many short markdown cells are good;
  what gets cut is explanation of something the student has not yet seen.
- **Words first, symbols at the naming step.**
  Until the phenomenon is named,
  the markdown above a cell says in words what it computes
  ("the average of the `N` tosses").
  The formula arrives with the name, beside the line that already computes it.
- **Edit a literal before reaching for a widget.**
  Changing `N = 10` to `N = 100` shows exactly what changed.
  A widget (in Colab, a form field) earns its place
  when the lesson needs many repetitions or a sweep
  that rerunning by hand would bury.
  Reading a widget's value is itself a construct; count it in step 6.
- **"Run it again" needs fresh randomness.**
  Create one seeded generator (`rng = np.random.default_rng(seed)`) in an early cell
  and draw from it in later cells, never from the global `np.random` functions.
  Rerunning a draw cell then gives a new sample,
  while a top-to-bottom run reproduces every figure.
  A seed set inside the cell the student reruns makes every rerun identical,
  and the demo teaches the opposite of its point.
- **A plot carries one idea.**
  No legend, color, annotation, or extra panel the observation does not need.

When unsure, choose the version that is shorter, slower, more concrete,
more visible, and easier to modify.
Cut scope before adding explanation.

## Order of work

- Designing: state the final observation and the step ladder
  (one line per step, active moments marked) before writing any cell,
  so the design can be vetoed cheaply.
- Reviewing: findings against the workflow steps and the rules above,
  most damaging first.
