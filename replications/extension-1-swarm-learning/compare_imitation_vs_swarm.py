"""The runnable experiment: imitation (../../update_rule.py, via ../../main.py)
vs. swarm (swarm_update_rule.py, via main_swarm.py), same fixed Prisoner's
Dilemma, same scale_free network, same reduced-scale settings as
../../reduced_scale_figures.py -- see ARCHITECTURE.txt for why each choice."""
import sys
import time

sys.path.insert(0, "../..")
from main import run_batch, average_trace

from main_swarm import run_batch_swarm
from plot_comparison import plot_traces

R, S, T, P = 1, -0.1, 1.2, 0
N = 500
NUM_REALIZATIONS = 10
TRANSIENT = 300
AVG_WINDOW = 60
GENERATIONS = TRANSIENT + AVG_WINDOW
M, AVG_DEGREE = 2, 4

if __name__ == "__main__":
    start = time.time()

    print("Running imitation...")
    imitation_traces = run_batch("scale_free", N, GENERATIONS, R, S, T, P, NUM_REALIZATIONS, seed=1, m=M, avg_degree=AVG_DEGREE)
    imitation_avg = average_trace(imitation_traces)
    print(f"  final cooperation (avg of last {AVG_WINDOW} gens): "
          f"{sum(imitation_avg[-AVG_WINDOW:]) / AVG_WINDOW:.3f}")

    print("Running swarm...")
    swarm_traces = run_batch_swarm("scale_free", N, GENERATIONS, R, S, T, P, NUM_REALIZATIONS, seed=1, m=M, avg_degree=AVG_DEGREE)
    swarm_avg = average_trace(swarm_traces)
    print(f"  final cooperation (avg of last {AVG_WINDOW} gens): "
          f"{sum(swarm_avg[-AVG_WINDOW:]) / AVG_WINDOW:.3f}")

    fig = plot_traces(
        {"Imitation (paper's rule)": imitation_avg, "Swarm (PSO)": swarm_avg},
        title=f"Imitation vs. swarm, scale_free, PD (T={T}, S={S})",
    )
    fig.savefig("figures/imitation_vs_swarm.png", dpi=150)
    print(f"saved figures/imitation_vs_swarm.png ({time.time() - start:.0f}s elapsed)")
