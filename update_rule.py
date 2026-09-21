"""Update rule -- pairwise comparison, Santos, Pacheco & Lenaerts (2006),
Methods, p. 3493: "a neighbor y is drawn at random among the k_x neighbors;
then, only if P_y > P_x, the strategy of chosen neighbor y replaces that of x
with probability (P_y-P_x)/[k>D>]", k>=max(k_x,k_y), D>=max(T,1)-min(S,0)."""


def next_strategy(graph, x, strategies, payoffs, T, S, rng):
    """
    x: the agent being updated.
    rng: a random.Random instance (shared across the whole run, for
    reproducibility -- see network.py's seed for why).
    Returns the strategy x should hold next generation.
    """
    y = rng.choice(list(graph.neighbors(x)))
    Px, Py = payoffs[x], payoffs[y]
    if Py <= Px:
        return strategies[x]
    k_gt = max(graph.degree[x], graph.degree[y])
    D_gt = max(T, 1) - min(S, 0)
    prob = (Py - Px) / (k_gt * D_gt)
    return strategies[y] if rng.random() < prob else strategies[x]
