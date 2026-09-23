"""Swarm (PSO-style) update rule -- the swarm analogue of ../update_rule.py's
next_strategy(). See ARCHITECTURE.txt for why: local-best (graph neighbors,
agent included) not global-best, fitness is this generation's payoff, not a
cumulative score."""


def next_position(graph, x, positions, velocities, personal_best_position, payoffs, w, c1, c2, rng):
    """
    x: the agent being updated.
    positions, velocities: dicts of every agent's CURRENT position/velocity
    (this generation), position in [0,1], velocity in [-1,1].
    personal_best_position: dict, x's own best-ever position -- the caller
    is expected to have already updated this using this generation's payoff
    before calling next_position().
    payoffs: dict, every agent's payoff this generation (from payoff.py) --
    used to find x's neighborhood-best (the "social" pull target).
    w, c1, c2: PSO inertia / cognitive / social coefficients.
    rng: a random.Random instance, shared across the whole run, for
    reproducibility.
    Returns (new_position, new_velocity) for x.
    """
    candidates = list(graph.neighbors(x)) + [x]
    best = max(candidates, key=lambda n: payoffs[n])
    local_best_position = positions[best]

    r1, r2 = rng.random(), rng.random()
    new_velocity = (
        w * velocities[x]
        + c1 * r1 * (personal_best_position[x] - positions[x])
        + c2 * r2 * (local_best_position - positions[x])
    )
    new_velocity = max(-1.0, min(1.0, new_velocity))

    new_position = positions[x] + new_velocity
    new_position = max(0.0, min(1.0, new_position))

    return new_position, new_velocity
