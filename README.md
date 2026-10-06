## Course description
This course is an introduction to data analysis emphasizing the nature of science, statistical literacy, thinking, and reasoning. While focused on statistical concepts such as probability, distributions, and hypothesis testing, examples and applications are based on competencies relevant to biological data, experimental design and interpretations in light of biological models. The course applies active learning, with both lectures and recitation periods built around student engagement and hands-on activities. These include, but are not limited to, computer-based exercises, writing protocol design, plotting, analyzing, and interpreting published and simulated data.

Prerequisite: Computational Thinking and basic Python coding

## Learning objectives:
 * Be able to reason with probabilistic statements;
 * See the world with conditional probability;
 * Apply the law of large numbers to averages;
 * Use sampling distributions to describe p-value and statistical power;
 * Use pseudo-random numbers to simulate probabilistic outcomes;
 * Write and debug short Python programs that generate and inspect samples;
 * Use shuffling to generate sampling distributions under independence;
 * Develop, formulate, execute, and interpret statistical tests of biological hypotheses using quantitative data;
 * Determine when to use null hypothesis tests and how to report effect sizes;
 * Design an experiment's sample size and write a practical protocol for approval;
 * Analyze, and interpret biological data to communicate with others;
 * Calculate required sample size through power analysis; and
 * Evaluate and critique statistical results in the scientific literature and its derivatives as a reader or a reviewer.

## Schedule
 * Day 1: Conditional probability
 * Day 2: Hypothesis testing
 * Day 3: Experimental design

## Resources
 * Simon, J. L. (1997). Resampling: The new statistics. Resampling Stats. https://resample.com/intro-text-online/
 * Wasserman, L. (2010). All of Statistics: A Concise Course in Statistical Inference (Springer Texts in Statistics). Springer. https://www.stat.cmu.edu/~larry/all-of-statistics/
 * Andrew Gelman, Jennifer Hill, Aki Vehtari (2024): Regression and Other Stories https://avehtari.github.io/ROS-Examples/
 * Ryan Tibshirani's course: https://www.stat.cmu.edu/~ryantibs/datamining/
 * Statistical Rethinking (Bayesian) course materials (including videos) https://github.com/rmcelreath/stat_rethinking_2024
 * The BMJ Statistics at Square One: https://thebmj-frontend.bmj.com/about-bmj/resources-readers/publications/statistics-square-one https://indp-stat-2025.streamlit.app (https://github.com/hyungju-jeon/indp-stat)

### Resampling reading guide

The widgets use Julian L. Simon's *Resampling: The New Statistics* as a
companion for the simulation-first view of probability and inference.

# Activities

## Day 1 morning

### Conditioning is Zooming in
https://catniplab.github.io/teaching/possible-worlds/

### Random sampling and histogram plotting
[Open in Colab](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/01_random_sampling.ipynb)

### Central limit theorem and Law of large numbers
[Open in Colab](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/02_averages.ipynb)

## Day 2 morning:

### Hands-on exercises: Is the dealer trying to cheat with a loaded coin?
[Worksheet (PDF)](https://github.com/memming/stats-and-prob-lecture/releases/download/day2-worksheet-2026/coin_test.pdf):
paper and pencil, about 25 minutes.
Source and instructor key: [worksheets/](worksheets/) (`make student`, `make key`).

### Shuffling and Permutation, how to break dependence
[Open in Colab](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/03_shuffling.ipynb)

### Implement your own hypothesis test
This exercise is after the hands-on exercise.

## Day 2 afternoon: Statistics and AI driver's license

Learning with AI: make the AI teach instead of tell, read code before trusting it,
and check your understanding without AI.
[Slides (PDF)](slides/day2_afternoon_learning_with_ai.pdf).

### Reading code with AI: your morning test and an AI version
[Open in Colab](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/04_code_reading.ipynb)

### Type-I, Type-II errors and statistical power
The dealer's coin again: false accusations, the power curve, and the trade-off between α and β,
each worked first without AI and then checked or extended with an AI step.
[Open in Colab](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/05_errors_and_power.ipynb)

### Type I and Type II errors with real mice
[Open in Colab](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/06_real_data.ipynb)
Data: [data/bdnf_mice.csv](data/bdnf_mice.csv) (Higuera, Gardiner & Cios 2015, CC BY 4.0).

### Invent your own procedure for multiple testing
Optional, if time allows: the last slides before the wrap-up.

## Day 3 morning:

### Paired vs Unpaird t-test

### Power analysis
