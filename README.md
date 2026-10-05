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
 * Wasserman, L. (2010). All of Statistics: A Concise Course in Statistical Inference (Springer Texts in Statistics). Springer. https://www.stat.cmu.edu/~larry/all-of-statistics/
 * Simon, J. L. (1997). Resampling: The new statistics. Resampling Stats. https://resample.com/intro-text-online/
 * Andrew Gelman, Jennifer Hill, Aki Vehtari (2024): Regression and Other Stories https://avehtari.github.io/ROS-Examples/
 * Ryan Tibshirani's course: https://www.stat.cmu.edu/~ryantibs/datamining/
 * Statistical Rethinking (Bayesian) course materials (including videos) https://github.com/rmcelreath/stat_rethinking_2024
 * The BMJ Statistics at Square One: https://thebmj-frontend.bmj.com/about-bmj/resources-readers/publications/statistics-square-one https://indp-stat-2025.streamlit.app (https://github.com/hyungju-jeon/indp-stat)

## Hands-on exercises
### Is the dealer trying to cheat with a loaded coin?

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

### Sampling distribution of the mean

### Shuffling and Permutation, how to break dependence

### Implement your own hypothesis test
This exercise is after the hands-on exercise.

### Type-I, Type-II errors and staistical power

### Paired vs Unpaird t-test

### Invent your own procedure for multiple testing
