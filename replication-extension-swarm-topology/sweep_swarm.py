"""Swarm (T, S) sweep -- the swarm analogue of ../sweep.py's sweep().
Same grid loop, same tail-averaging; the only change is that each grid
point calls run_batch_swarm() instead of the paper's run_batch()."""
import sys

sys.path.insert(0, "..")
sys.path.insert(0, "../replication-extension-swarm")
from main import average_trace
from main_swarm import run_batch_swarm


def sweep_swarm(network_kind, n, generations, T_values, S_values, R, P, num_realizations, seed,
                m=4, avg_degree=8, tail=20, w=0.7, c1=1.5, c2=1.5):
    """
    Runs run_batch_swarm() at every (T, S) combination in the grid.
    tail: average the last `tail` generations of the averaged trace (same
    reason as ../sweep.py -- a single last point is noisier than needed).
    w, c1, c2: PSO coefficients, defaults as in ../replication-extension-swarm/.
    Returns {(T, S): average cooperation fraction}, the same shape as
    ../sweep.py, so ../plot.py can draw it unchanged.
    """
    results = {}
    for T in T_values:
        for S in S_values:
            traces = run_batch_swarm(network_kind, n, generations, R, S, T, P,
                                      num_realizations, seed, w=w, c1=c1, c2=c2,
                                      m=m, avg_degree=avg_degree)
            avg = average_trace(traces)
            results[(T, S)] = sum(avg[-tail:]) / tail
    return results
