"""Reproduces the SHAPE of Fig. 2 and Fig. 3 at a reduced scale.

Why reduced: the paper's real protocol (N=10,000, 100 realizations,
10,000-generation transient + 1,000-generation averaging window, per
(T, S) grid point) is not feasible in this pure-Python, dict-based
implementation -- timed at roughly 4 hours per grid point for scale-free
networks, and tens of hours for a single complete-graph realization (see
ARCHITECTURE.txt's "TIMING CHECK", 2026-09-21). This script keeps the
paper's *structure* (independent realizations, transient + averaging
window, same T/S range) but shrinks every parameter until the whole
thing runs in minutes. This is a documented deviation, not the paper's
actual figures -- expect the SHAPE to match Figs. 2/3, not the exact
numbers. Smaller N means more finite-size noise, especially near domain
boundaries.

Deviations from the paper's protocol:
    paper                          this script
    N = 10,000 (all networks)      N = 500 (heterogeneous), N = 200 (complete)
    z = 4 (heterogeneous)          z = 4 (m=2, avg_degree=4) -- unchanged
    10,000 transient generations   300
    1,000 averaged generations     60
    100 realizations               10
    (T, S) grid: fine, unstated    5x5 = 25 points
Complete graphs get a smaller N than the heterogeneous ones because
their edge count grows as N^2, not N*z -- at N=500 a single complete-graph
realization alone would take about 15 seconds/generation x 360
generations, too slow for 10 realizations x 25 grid points.
"""
import time

from sweep import sweep
from plot import plot_pair
import matplotlib.pyplot as plt

T_values = [0.0, 0.5, 1.0, 1.5, 2.0]
S_values = [-1.0, -0.5, 0.0, 0.5, 1.0]
NUM_REALIZATIONS = 10
TRANSIENT = 300
AVG_WINDOW = 60
GENERATIONS = TRANSIENT + AVG_WINDOW


def run_panel(network_kind, n):
    return sweep(network_kind, n=n, generations=GENERATIONS, T_values=T_values, S_values=S_values,
                 R=1, P=0, num_realizations=NUM_REALIZATIONS, seed=1, tail=AVG_WINDOW,
                 m=2, avg_degree=4)


if __name__ == "__main__":
    start = time.time()

    print("Fig. 2 -- complete...")
    results_complete = run_panel("complete", n=200)
    print("Fig. 2 -- single_scale...")
    results_single_scale = run_panel("single_scale", n=500)
    plot_pair(results_complete, results_single_scale, T_values, S_values,
              title_left="Complete", title_right="Single-scale",
              suptitle="Evolution of cooperation, reduced scale -- cf. Fig. 2")
    plt.savefig("fig2_reduced_scale.png", dpi=150)
    print(f"saved fig2_reduced_scale.png ({time.time() - start:.0f}s elapsed)")

    print("Fig. 3 -- scale_free_random...")
    results_sf_random = run_panel("scale_free_random", n=500)
    print("Fig. 3 -- scale_free (Barabasi-Albert)...")
    results_sf = run_panel("scale_free", n=500)
    plot_pair(results_sf_random, results_sf, T_values, S_values,
              title_left="Random scale-free", title_right="Barabasi-Albert scale-free",
              suptitle="Evolution of cooperation, reduced scale -- cf. Fig. 3")
    plt.savefig("fig3_reduced_scale.png", dpi=150)
    print(f"saved fig3_reduced_scale.png ({time.time() - start:.0f}s total)")
