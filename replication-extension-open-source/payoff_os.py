"""Payoff accumulation with programs instead of C/D. Same rule as
../payoff.py (every agent plays every neighbour once per generation,
payoffs accumulate); the only change is that each meeting's two actions
come from programs.py's outcome table first."""
import sys

sys.path.insert(0, "..")
from payoff import OUTCOME

from programs import outcome

# Programs that read the opponent's code. Only these pay the proof cost.
CODE_READERS = {"CliqueBot", "FairBot", "PrudentBot"}


def compute_payoffs(graph, programs, R, S, T, P, cost=0.0):
    """
    graph: networkx Graph.
    programs: dict {node: program name from programs.PROGRAMS}.
    cost: subtracted from a code-reading program's payoff once per game it
    plays (reading/proving isn't free -- Critch et al. Open Problem 9).
    Returns dict {node: accumulated payoff this generation}.
    """
    matrix = {"R": R, "S": S, "T": T, "P": P}
    payoff = {node: 0.0 for node in graph.nodes}
    for x, y in graph.edges:
        ax, ay = outcome(programs[x], programs[y])
        payoff[x] += matrix[OUTCOME[(ax, ay)]]
        payoff[y] += matrix[OUTCOME[(ay, ax)]]
        payoff[x] -= cost * (programs[x] in CODE_READERS)
        payoff[y] -= cost * (programs[y] in CODE_READERS)
    return payoff


def cooperation_fraction(graph, programs):
    """
    Fraction of all actions played this generation that were C. Every edge
    is one meeting with two actions (one per side), so the denominator is
    2 * number of edges. This replaces "fraction of cooperators": a FairBot
    plays C with some neighbours and D with others.
    """
    c_actions = 0
    for x, y in graph.edges:
        ax, ay = outcome(programs[x], programs[y])
        c_actions += (ax == "C") + (ay == "C")
    return c_actions / (2 * graph.number_of_edges())
