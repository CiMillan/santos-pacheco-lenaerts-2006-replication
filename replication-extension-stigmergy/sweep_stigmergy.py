"""Stigmergy (T, S) sweep -- the stigmergy analogue of ../sweep.py's sweep().
Same grid loop, same tail-averaging; the only change is that each grid
point calls run_batch_stigmergy() instead of the paper's run_batch()."""
import sys

sys.path.insert(0, "..")
from main import average_trace
from main_stigmergy import run_batch_stigmergy


def sweep_stigmergy(network_kind, n, generations, T_values, S_values, R, P, num_realizations, seed, lam,
                    initial_c_fraction=0.5, m=4, avg_degree=8, tail=20, trace_rule="average"):
    """
    Runs run_batch_stigmergy() at every (T, S) combination in the grid.
    Returns {(T, S): average cooperation fraction}, the same shape as
    ../sweep.py, so ../plot.py can draw it unchanged.
    """
    results = {}
    for T in T_values:
        for S in S_values:
            traces = run_batch_stigmergy(network_kind, n, generations, R, S, T, P,
                                         num_realizations, seed, lam, initial_c_fraction, m, avg_degree, trace_rule)
            avg = average_trace(traces)
            results[(T, S)] = sum(avg[-tail:]) / tail
    return results
