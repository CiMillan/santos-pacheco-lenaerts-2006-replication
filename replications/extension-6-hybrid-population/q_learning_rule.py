"""Update rule for AI agents -- stateless Q-learning with softmax choice.
Q update: Bloembergen, Tuyls, Hennes & Kaisers (2015), JAIR 53, eq. 3, with
no next state (gamma = 0), since each generation is one repeated game.
Softmax ("Boltzmann exploration") with temperature tau: same paper, eq. 4.
Humans keep the paper's imitation rule (../../update_rule.py)."""
import math


def softmax_action(q, tau, rng):
    """
    q: {"C": value, "D": value}, this agent's learned action values.
    tau: temperature. Small tau = nearly always the best-valued action;
    large tau = nearly a coin flip.
    Two actions, so softmax reduces to p(C) = 1 / (1 + exp(-(Q_C - Q_D) / tau)).
    Returns "C" or "D".
    """
    p_c = 1 / (1 + math.exp(-(q["C"] - q["D"]) / tau))
    return "C" if rng.random() < p_c else "D"


def update_q(q, action, reward, alpha):
    """
    Moves the value of the action just played a step alpha toward the reward
    it earned: Q(a) <- Q(a) + alpha * (reward - Q(a)).
    The other action's value is left unchanged. Returns a new dict.
    """
    new_q = dict(q)
    new_q[action] = q[action] + alpha * (reward - q[action])
    return new_q
