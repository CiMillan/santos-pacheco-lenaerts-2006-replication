"""Parameter sweep with programs -- ../sweep.py's sweep(), calling
main_os.py's run_batch() instead. The cooperation results have the same
shape as ../sweep.py's, so ../plot.py works on them unchanged; the final
program shares come back alongside."""
import sys

sys.path.insert(0, "..")
from main import average_trace

from programs import PROGRAMS
from main_os import run_batch


def sweep_os(network_kind, n, generations, T_values, S_values, R, P, num_realizations, seed,
             m=4, avg_degree=8, tail=20, cost=0.0):
    """
    tail: average the last `tail` generations, as in ../sweep.py.
    cost: per-game proof cost for code-reading programs (default 0 = free).
    Returns (cooperation, shares):
      cooperation = {(T, S): cooperation per meeting, averaged}
      shares      = {(T, S): {program: final share, averaged over realizations}}
    """
    cooperation, shares = {}, {}
    for T in T_values:
        for S in S_values:
            runs = run_batch(network_kind, n, generations, R, S, T, P, num_realizations, seed, m, avg_degree, cost)
            avg = average_trace([trace for trace, _ in runs])
            cooperation[(T, S)] = sum(avg[-tail:]) / tail
            shares[(T, S)] = {p: sum(s[p] for _, s in runs) / len(runs) for p in PROGRAMS}
    return cooperation, shares
