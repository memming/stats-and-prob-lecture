# Notebook 5: Type I and Type II errors and power - design

Status: drafted 2026-10-06 by Hyungju Jeon for the Day 2 afternoon session; not yet reviewed by Memming.
Implemented in `notebooks/05_errors_and_power.py`, paired with `.ipynb` for Colab.
The slides for this part are in `slides/day2_afternoon_learning_with_ai.pdf`.

## Where it sits

Day 2 afternoon, after notebook 4. It reuses the dealer's coin from the morning worksheet
(watch 10 flips; accuse on 0, 1, 9, or 10 heads).
It serves the `README.md` objective "Use sampling distributions to describe p-value and statistical power".

## Observation and steps

Takeaway: a simulation is a quick way to check a hand calculation, and to see what changes when you change one thing.

The questions live on the slides, and students answer them on paper with AI closed.
This notebook does only what the slides cannot:
- a simulation cell per topic (α of the rule; the power curve; the α–β trade-off;
  the optional questions on accused dealers, caught cheaters, and peeking),
  run after the paper answer, each with one suggested change;
- the AI prompts in copyable boxes (tutor on "can β be one number?",
  HTML pages for the power curve and the trade-off, explain-back).

There are no restated questions and no collapsed answers:
the simulation output is the check, so students still compare it with their own number.
The answers are in the slides' presenter notes.

## Pilot finding that shaped the AI steps

Asked "What is type I and type II error?", Claude Haiku, Sonnet, and Opus (low effort) and GPT
all presented β as a single number; none said it depends on the size of the effect.
So the derivation comes first, and the AI's textbook answer is never the starting point.
