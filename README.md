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
The locally stored copy is reference material and is not distributed with this
repository. The chapter numbers below are a quick way to find the relevant
discussion in a legitimate copy of the book.

| Course topic | Read first | Useful follow-up |
| --- | --- | --- |
| Random sampling and histograms | Chapter 4, "The Monte Carlo Simulation Method (Resampling)" | Chapter 9, "Sampling Variability and Small Samples"; Chapter 10, "A Definition and General Procedure for Monte Carlo Simulation" |
| Conditional probability and independence | Chapter 4, "Conditional and Unconditional Probabilities" | Chapter 5, "The Special Case of Independence"; Chapter 6, "The Concepts of Replacement and Non-Replacement" |
| Law of large numbers and sampling distributions | Chapter 9, "On Variability in Sampling" | Chapter 20, "Estimating the Accuracy of a Sample Mean"; Chapter 21, "The Distance Between Sample and Population Mean" |
| Shuffling and permutation null distributions | Chapter 15, "Should a Single Sample of Counted Data be Considered Different From a Benchmark Universe?" | Chapter 17, hypothesis testing with paired comparisons; Chapter 19, "Skeleton Procedure for Testing Hypotheses" and "Choice of the Benchmark Universe" |
| Hypothesis tests, p-values, and power | Chapter 16, "The Logic of Hypothesis Tests" and "The Concept of Statistical Significance" | Chapter 18, hypothesis testing with measured data; Chapter 24, "How Large a Sample?" |

For every chapter, start with the physical or biological process being modeled,
then identify what is repeatedly sampled or shuffled, and only then interpret
the resulting distribution. That is the common thread between the reading and
the course widgets.

## Hands-on exercises
### Is the dealer trying to cheat with a loaded coin?
[Worksheet (PDF)](https://github.com/memming/stats-and-prob-lecture/releases/download/day2-worksheet-2026/coin_test.pdf):
paper and pencil, about 25 minutes.
Source and instructor key: [worksheets/](worksheets/) (`make student`, `make key`).

## Colab notebooks
Students open the notebooks in Google Colab, signed in with a Google account,
and save their own copy to Drive.
Each exercise teaches a statistical idea and gives students a small amount
of meaningful Python to write and debug.
See [demo-design.md](demo-design.md) for the teaching sequence
and [colab.md](colab.md) for authoring and classroom deployment.

### Random sampling and histogram plotting
[Open in Colab](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/01_random_sampling.ipynb)

We would like to learn the python library for random sampling.
Let's toss some coins and dice. Fun visualization.

see also:
 * https://ubcmath.github.io/python/probability/discrete.html
 * https://www.eg.bucknell.edu/~phys310/skills/data_analysis/coin_flip_CLT.html
 * https://github.com/buruzaemon/IntroductionToProbabilityPy
 * https://risk-engineering.org/notebook/coins-dice.html

### Central limit theorem and Law of large numbers
[Open in Colab](https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/02_averages.ipynb)

### Sampling distribution of the mean

### Shuffling and Permutation, how to break dependence

### Implement your own hypothesis test
This exercise is after the hands-on exercise.

Day 2 afternoon:

### Type-I, Type-II errors and staistical power

### Paired vs Unpaird t-test

### Invent your own procedure for multiple testing
