"""Update rule -- pairwise comparison (Fermi), Pinheiro, Santos & Pacheco (2012),
section 2.2: an individual i imitates a randomly chosen neighbour j with
probability p(i, j) = [1 + e^(-beta (f_j - f_i))]^-1, f = accumulated payoff.
beta = 0: random drift; large beta: always copy a fitter neighbour.
Drop-in replacement for ../../update_rule.py's next_strategy()."""
import math


def fermi_probability(beta, f_x, f_y):
    """Probability that x copies y. Written in the overflow-safe form:
    for a large negative exponent, exp() would overflow, so use the
    equivalent e^z / (1 + e^z) instead."""
    z = beta * (f_y - f_x)
    if z >= 0:
        return 1 / (1 + math.exp(-z))
    return math.exp(z) / (1 + math.exp(z))


def next_strategy_fermi(graph, x, strategies, payoffs, beta, rng):
    """
    x: the agent being updated. rng: the run's shared random.Random.
    Unlike the Santos rule, x may also copy a worse-off neighbour
    (with probability below 0.5) -- that is the noise beta controls.
    Returns the strategy x should hold next generation.
    """
    y = rng.choice(list(graph.neighbors(x)))
    prob = fermi_probability(beta, payoffs[x], payoffs[y])
    return strategies[y] if rng.random() < prob else strategies[x]
