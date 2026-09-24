"""Network-engineering bots -- Shirado & Christakis (2020), Experiment 1.
Each agent gets its own bot: one tie, always cooperates, never imitates.
See ARCHITECTURE.txt for the decisions behind each rule."""


def add_bots(graph):
    """
    Attaches one bot to every agent, in place. Agents keep their labels
    0..n-1; the bot of agent i is node n+i, linked only to i (bots are
    never linked to each other).
    Returns the list of bot nodes.
    """
    n = graph.number_of_nodes()
    bots = [n + i for i in range(n)]
    graph.add_edges_from((i, n + i) for i in range(n))
    return bots


def pick(pool, is_valid, rng, tries=20):
    """
    A uniformly random member of `pool` that passes is_valid(), or None if
    there is none. Tries a few random draws first (fast when most of the
    pool is valid), then falls back to filtering the whole pool.
    """
    for _ in range(tries):
        j = rng.choice(pool)
        if is_valid(j):
            return j
    valid = [j for j in pool if is_valid(j)]
    return rng.choice(valid) if valid else None


def bot_offer(graph, agent, condition, strategies, cooperators, n, rng):
    """
    The offer made by `agent`'s bot this generation. The agent always
    accepts, so the offer is applied to the graph in place.
    condition: "always_c", "random", "engaged" or "disengaged".
    cooperators: list of agents playing C now (computed once per
    generation by the caller; strategies don't change during rewiring).
    n: number of agents -- nodes below n are agents, the rest are bots.
    Returns ("cut", j), ("link", j), or None if the bot did nothing.
    Only agent-agent ties change; the bot's own tie never does.
    """
    if condition == "always_c":
        return None

    if condition == "random":
        # Coin flip, blind to strategy: cut a random agent neighbour or link a
        # random non-neighbour. Not the paper's "random agent: cut if linked,
        # else link" -- at n=500 almost nobody is linked, so that rule would
        # only ever add ties (see ARCHITECTURE.txt).
        if rng.random() < 0.5:
            agent_neighbours = [j for j in graph.neighbors(agent) if j < n]
            if not agent_neighbours:
                return None
            j = rng.choice(agent_neighbours)
            graph.remove_edge(agent, j)
            return ("cut", j)
        j = pick(range(n), lambda j: j != agent and not graph.has_edge(agent, j), rng)
        if j is None:
            return None
        graph.add_edge(agent, j)
        return ("link", j)

    if condition == "engaged":
        if not cooperators:
            return None
        j = pick(cooperators, lambda j: j != agent and not graph.has_edge(agent, j), rng)
        if j is None:
            return None
        graph.add_edge(agent, j)
        return ("link", j)

    if condition == "disengaged":
        defector_neighbours = [j for j in graph.neighbors(agent) if j < n and strategies[j] == "D"]
        if not defector_neighbours:
            return None
        j = rng.choice(defector_neighbours)
        graph.remove_edge(agent, j)
        return ("cut", j)

    raise ValueError(f"unknown condition: {condition}")
