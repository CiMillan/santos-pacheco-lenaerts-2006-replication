"""Stigmergic update rule -- the stigmergy analogue of ../update_rule.py's
next_strategy(). Each node keeps a fading TRACE of the payoffs earned there;
neighbours read that trace instead of the node's current payoff. Idea from
Pal, Wang & Buehler (2026), SwarmWorld: agents learn mostly from traces left
in the environment rather than by direct contact. See ARCHITECTURE.txt."""


def update_traces(traces, payoffs, lam):
    """
    traces: dict {node: trace value}, the record each node has left so far.
    payoffs: dict {node: payoff earned this generation}.
    lam: in (0, 1], how fast a trace follows new payoffs. lam=1 means the
    trace is just the current payoff (the paper's rule); a small lam means
    the trace remembers old payoffs for a long time.
    Returns the new traces: trace <- (1 - lam) * trace + lam * payoff.
    """
    return {node: (1 - lam) * traces[node] + lam * payoffs[node] for node in traces}


def next_strategy(graph, x, strategies, payoffs, traces, T, S, rng, offered=None):
    """
    Same as ../update_rule.py's next_strategy(), with one change: x compares
    its own CURRENT payoff with neighbour y's TRACE, not y's current payoff.
    offered: the strategy x copies from y if it switches. Default: y's current
    strategy. The strategy-memory control passes y's REMEMBERED strategy.
    The probability (trace_y - P_x) / (k> D>) stays in [0, 1]: a trace is an
    average of y's past payoffs, so it lies in the same range as a payoff.
    Returns the strategy x should hold next generation.
    """
    y = rng.choice(list(graph.neighbors(x)))
    Px, Ty = payoffs[x], traces[y]
    if Ty <= Px:
        return strategies[x]
    k_gt = max(graph.degree[x], graph.degree[y])
    D_gt = max(T, 1) - min(S, 0)
    prob = (Ty - Px) / (k_gt * D_gt)
    offered = strategies if offered is None else offered
    return offered[y] if rng.random() < prob else strategies[x]


def update_traces_peak(traces, payoffs, lam):
    """
    Control for update_traces(): the same fading average, except that a new
    HIGH payoff is taken in full at once. The trace jumps up to any payoff
    above it and only fades down at rate lam, so it holds on to windfalls --
    like PSO's personal best (a running maximum), but still forgetting.
    lam=1 is again just the current payoff (the paper's rule).
    """
    return {
        node: max(payoffs[node], (1 - lam) * traces[node] + lam * payoffs[node])
        for node in traces
    }


def update_memory_peak(traces, remembered, payoffs, strategies, lam):
    """
    Strategy-memory control: the peak trace (update_traces_peak), plus the
    strategy that earned it. When this generation's payoff sets a new peak,
    the node remembers its current strategy; otherwise it keeps the old one.
    This is the closest match to PSO's personal best, which stores the
    POSITION (strategy) where the best payoff was earned, not just the payoff.
    lam=1: every payoff is a new peak, so the remembered strategy is always
    the current one (the paper's rule).
    Returns (new traces, new remembered strategies).
    """
    new_traces, new_remembered = {}, {}
    for node in traces:
        faded = (1 - lam) * traces[node] + lam * payoffs[node]
        if payoffs[node] >= faded:
            new_traces[node], new_remembered[node] = payoffs[node], strategies[node]
        else:
            new_traces[node], new_remembered[node] = faded, remembered[node]
    return new_traces, new_remembered
