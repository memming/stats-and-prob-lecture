# Notebook 5: Type I and Type II errors and power - design

Status: drafted 2026-10-06 by Hyungju Jeon for the Day 2 afternoon session; not yet reviewed by Memming.
Implemented in `notebooks/05_errors_and_power.py`, paired with `.ipynb` for Colab.
The slides for this part are in `slides/day2_afternoon_learning_with_ai.pdf`.

## Where it sits

Day 2 afternoon, after notebook 4. It reuses the dealer's coin from the morning worksheet
(watch 10 flips; accuse on 0, 1, 9, or 10 heads).
It serves the `README.md` objective "Use sampling distributions to describe p-value and statistical power".

## Observation and steps

Takeaway: the rule sets how often you accuse an honest dealer;
how often you catch a cheater depends on the cheat, and only more data makes it easy.

Each part is worked first with AI closed; then an AI step checks or extends it.

1. α from the fair-coin table: 0.022, not 0.05, because heads come in whole numbers.
2. The two errors; a prediction (can β be one number?);
   β for a 70% coin (0.85); everyone computes the power curve
   (0.048, 0.15, 0.38, 0.74 for 60%, 70%, 80%, 90% heads).
   AI step: the student writes their own idea, then asks an AI tutor whether β can be one number.
   In the pilot, tutors led to ideas students had not met
   (report β at the smallest cheat you care about, the worst case, or an average over cheats).
3. Reading the power curve; AI step: an HTML page with a slider for the number of flips.
   The α–β trade-off (accuse also on 2 or 8 heads: α 0.109, power 0.38);
   AI step: an HTML page with a movable rejection region.
   AI step: the student explains Type I and Type II errors to the AI and gets feedback only at the end.
4. Optional, three harder questions for everyone: how many accused dealers cheat (43% when 1 in 10 cheats);
   caught cheaters overestimate the cheat (0.92 instead of 0.70);
   peeking after 10 more flips raises α to 0.054.
5. Code checks for every answer.

## Pilot finding that shaped the AI steps

Asked "What is type I and type II error?", Claude Haiku, Sonnet, and Opus (low effort) and GPT
all presented β as a single number; none said it depends on the size of the effect.
So the derivation comes first, and the AI's textbook answer is never the starting point.
