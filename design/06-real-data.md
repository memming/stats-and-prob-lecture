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

0. Vibe research: upload the zip to an AI and ask it to analyse the data; keep its claim.
1. Clean: the AI writes code that merges the files into one table; the notebook checks 72 mice × 15 readings.
2. Look: the AI plots each mouse's readings and mean by group; what is one observation?
3. Hypothesis: written by the student first, then attacked by the AI.
4. Test: the AI writes `my_test`; the notebook runs it on random fake splits of saline mice
   (about 5% significant with one mean per mouse, about 47% when each reading counts as a mouse).
5. Show: the AI plots the result; the student writes two sentences, the AI attacks them; compare with step 0.

## Pilot (vibe research)

Asked "Among Control-genotype mice, does memantine change BDNF compared with saline? Analyse it and give me a p-value"
with the clean table, Claude Haiku (2 of 2 runs) treated 570 readings as independent and reported p = 0.0026, "memantine lowers BDNF";
Claude Sonnet, Opus, and GPT (6 of 6) averaged each mouse first and reported p = 0.29.
