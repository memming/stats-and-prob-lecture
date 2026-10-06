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

## Day 2 afternoon:

### Type-I, Type-II errors and staistical power

### Invent your own procedure for multiple testing

## Day 3 morning:

### Paired vs Unpaird t-test

### Power analysis
