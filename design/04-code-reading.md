# Notebook 4: reading code with AI - design

Status: drafted 2026-10-06 by Hyungju Jeon for the Day 2 afternoon session; not yet reviewed by Memming.
Implemented in `notebooks/04_code_reading.py`, paired with `.ipynb` for Colab.

## Where it sits

Day 2 afternoon, right after "Implement your own hypothesis test".
Students bring the test they wrote in the morning.
It serves the `README.md` objective "Write and debug short Python programs"
and the session's goal: use AI to learn, not to delegate.

## Observation and steps

Takeaway: you understand a test's code when you can predict what a change will do before you run it.

- Part A, the student's own test: run it on cases with a known answer
  (the coin worksheet, 9 heads in 10 flips: p = 0.022;
  the lean-mouse tumors from notebook 3: p = 4/252 = 0.016).
  The AI reviews without rewriting: it states the null hypothesis the code tests,
  and the student checks that this is what they meant.
- Bug reports to the AI follow one pattern:
  "I ran [this]. I expected [this], but got [that]. That is wrong because [reason]."
- Part B, an AI-written permutation test (real Claude Sonnet output, 5 October 2026, kept unchanged):
  predict, then change one line and run
  (`alternative="less"` versus `"greater"`, 20 shuffles with several seeds, removing the `+ 1`).
- The AI explains the code at three levels, draws an HTML page that animates one shuffle,
  and quizzes the student; answers are given without looking at the code.

## Pilot

The prompts were piloted with Claude (Opus, Sonnet, Haiku) and GPT through their command-line tools on 2026-10-05 and 2026-10-06.
Free-tier chat apps are being checked separately.
