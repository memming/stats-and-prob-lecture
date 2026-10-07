# Notebook 6: AI-assisted data analysis with real mice - design

Status: drafted 2026-10-07 by Hyungju Jeon for the Day 2 afternoon session; not yet reviewed by Memming.
Implemented in `notebooks/06_real_data.py`, paired with `.ipynb` for Colab.
Data: `data/bdnf_raw.zip` (source and licence in `data/bdnf_SOURCE.txt`).

## Where it sits

Day 2 afternoon, last part: practical data analysis with AI, after the Type I/II and power work on the coin.

## Observation and steps

Takeaway: the AI can do every step fast; you decide what to test, what counts as one observation, and you check each step.

The data are real (BDNF in mouse cortex; Control and Ts65Dn mice; memantine or saline; two learning conditions; 72 mice, 15 readings each),
exported messily on purpose: one file per group, Excel for Control mice and tab-separated text for Ts65Dn,
long versus wide layout, different column names, an "M" prefix on some mouse IDs, the group only in the file name,
and missing readings as empty cells, NA, or n/a.

Every step has three parts: the student decides first, the AI writes the code, and the student checks it.

1. Clean: the student writes what the table must hold; the AI merges the files; the notebook prints counts (72 mice × 15 readings) and shows one mouse's rows next to its raw file.
2. Look: the student plans the plot first (what is one dot, what is on each axis); the AI plots; the student checks dots per group and what one observation is.
3. Hypothesis: written by the student first, then attacked by the AI; the student keeps or changes it and says why.
4. Test: the student predicts p; the AI writes `my_test`; the notebook runs known-answer checks (this morning's tumours, p ≈ 0.016–0.02; identical groups, p ≈ 1)
   and random fake splits of saline mice (about 5% significant with one mean per mouse, about 47% when each reading counts as a mouse).
   A fresh chat can review the code ("Find bugs in this code. Do not fix them.").
5. Show: the student decides what the plot must show; the AI plots; the student checks it against the numbers from step 4.
6. Say what it means: two sentences, attacked by the AI.
