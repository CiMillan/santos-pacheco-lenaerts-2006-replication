"""Vectorized prototype of one generation -- the same model as ../payoff.py and
../update_rule.py (synchronous update, pairwise comparison), written with NumPy
arrays instead of Python loops. Used only to estimate full-scale run times."""
import numpy as np
import networkx as nx


def to_arrays(graph):
    """The graph as a sparse adjacency matrix plus each node's degree."""
    A = nx.to_scipy_sparse_array(graph, nodelist=range(graph.number_of_nodes()), format="csr", dtype=float)
    return A, np.diff(A.indptr).astype(float)


def step(A, deg, s, R, S, T, P, rng):
    """One generation on any graph. s: 1.0 = cooperator, 0.0 = defector."""
    nc = A @ s  # cooperating neighbours of each node
    pay = np.where(s == 1, nc * R + (deg - nc) * S, nc * T + (deg - nc) * P)
    y = A.indices[A.indptr[:-1] + (rng.random(len(s)) * deg).astype(np.int64)]  # one random neighbour each
    D = max(T, 1) - min(S, 0)
    prob = (pay[y] - pay) / (np.maximum(deg, deg[y]) * D)  # <= 0 never copies
    return np.where(rng.random(len(s)) < prob, s[y], s)


def step_complete(n, s, R, S, T, P, rng):
    """One generation on the complete graph. Everyone plays everyone, so payoffs
    depend only on the number of cooperators c -- no neighbour loop at all."""
    c = s.sum()
    pay = np.where(s == 1, (c - 1) * R + (n - c) * S, c * T + (n - c - 1) * P)
    y = rng.integers(0, n - 1, n)
    y += y >= np.arange(n)  # anyone except yourself
    D = max(T, 1) - min(S, 0)
    prob = (pay[y] - pay) / ((n - 1) * D)
    return np.where(rng.random(n) < prob, s[y], s)


def run(kind, n, generations, R, S, T, P, seed, m=2, avg_degree=4):
    """Like ../main.py's run(): returns the fraction of cooperators per generation."""
    import sys
    sys.path.insert(0, "..")
    from network import build_network
    rng = np.random.default_rng(seed)
    s = (rng.random(n) < 0.5).astype(float)
    trace = [s.mean()]
    if kind == "complete":
        for _ in range(generations):
            s = step_complete(n, s, R, S, T, P, rng)
            trace.append(s.mean())
        return trace
    A, deg = to_arrays(build_network(kind, n, seed=seed, m=m, avg_degree=avg_degree))
    for _ in range(generations):
        s = step(A, deg, s, R, S, T, P, rng)
        trace.append(s.mean())
    return trace
