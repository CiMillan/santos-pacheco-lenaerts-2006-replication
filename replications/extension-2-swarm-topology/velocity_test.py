"""Tests the hypothesis in CONCLUSIONS.txt: with c1 > 0 agents never stop
moving (two targets that disagree), and that ongoing motion is what breaks
stable cooperator clusters. Same loop as ../extension-1-swarm-learning/
main_swarm.py's run_swarm(), but it also records velocities and targets,
which run_swarm() doesn't return."""
import random
import sys

sys.path.insert(0, "../..")
sys.path.insert(0, "../extension-1-swarm-learning")
from network import build_network
from payoff import compute_payoffs
from swarm_update_rule import next_position
from main_swarm import positions_to_strategies


def motion_stats(network_kind, n, generations, T, S, c1, seed, window=60, w=0.7, c2=1.5, m=2, avg_degree=4):
    """
    Runs one swarm realization and measures the last `window` generations.
    Returns (mean_speed, stable_c_fraction, mean_target_gap):
      mean_speed: average |velocity| over all agents and window generations.
      stable_c_fraction: fraction of agents that were C in EVERY window
        generation (real cooperation, not flicker).
      mean_target_gap: average |personal best - neighbourhood best position|
        at the end -- how far apart an agent's two targets are.
    """
    rng = random.Random(seed)
    graph = build_network(network_kind, n, seed=seed, m=m, avg_degree=avg_degree)
    positions = {x: rng.random() for x in graph}
    velocities = {x: 0.0 for x in graph}
    pbest_pos = dict(positions)
    pbest_pay = {x: float("-inf") for x in graph}

    speeds, c_sets = [], []
    for gen in range(generations):
        payoffs = compute_payoffs(graph, positions_to_strategies(positions), 1, S, T, 0)
        for x in graph:
            if payoffs[x] > pbest_pay[x]:
                pbest_pay[x], pbest_pos[x] = payoffs[x], positions[x]
        updated = {x: next_position(graph, x, positions, velocities, pbest_pos, payoffs, w, c1, c2, rng) for x in graph}
        positions = {x: p for x, (p, v) in updated.items()}
        velocities = {x: v for x, (p, v) in updated.items()}
        if gen >= generations - window:
            speeds.append(sum(abs(v) for v in velocities.values()) / n)
            c_sets.append({x for x, p in positions.items() if p > 0.5})

    local_best_pos = {x: positions[max(list(graph.neighbors(x)) + [x], key=lambda nb: payoffs[nb])] for x in graph}
    gap = sum(abs(pbest_pos[x] - local_best_pos[x]) for x in graph) / n
    return sum(speeds) / window, len(set.intersection(*c_sets)) / n, gap


if __name__ == "__main__":
    SEEDS = [1, 2, 3]
    points = [("PD", 1.5, -0.5), ("Snowdrift", 1.5, 0.5)]
    print(f"scale_free, n=500, 360 generations, last 60 measured, mean of seeds {SEEDS}\n")
    print(f"{'point':<22} {'c1':>5} {'speed':>7} {'stable C':>9} {'target gap':>11}")
    for name, T, S in points:
        for c1 in [0.0, 0.25, 0.5, 1.0, 1.5]:
            stats = [motion_stats("scale_free", 500, 360, T, S, c1, seed) for seed in SEEDS]
            speed, stable, gap = (sum(s[i] for s in stats) / len(SEEDS) for i in range(3))
            print(f"{name + f' T={T},S={S}':<22} {c1:5.2f} {speed:7.3f} {stable:9.3f} {gap:11.3f}", flush=True)
