"""Times the current code and the vectorized prototype, and extrapolates both to
the paper's scale: N=10,000, 11,000 generations, 100 realizations, 5x5 grid."""
import sys
import time
import numpy as np

sys.path.insert(0, "..")
from main import run
from network import build_network
from reduced_scale_figures import run_panel
import vectorized_prototype as vp

RUNS = 11000 * 100 * 25  # generations x realizations x grid points
ARGS = dict(R=1, S=0.0, T=1.5, P=0)


def per_gen(fn, gens):
    fn(1)
    t = time.perf_counter()
    fn(gens)
    return (time.perf_counter() - t) / gens


if __name__ == "__main__":
    print("-- current code, reduced scale (whole 5x5 grid)")
    for kind, n in [("complete", 200), ("single_scale", 500), ("scale_free_random", 500), ("scale_free", 500)]:
        t = time.time()
        run_panel(kind, n)
        print(f"{kind} n={n}: {time.time() - t:.0f} s", flush=True)

    print("-- network build time at N=10,000 (once per realization)")
    build = {"complete": 0.0}
    for kind in ["single_scale", "scale_free_random", "scale_free"]:
        t = time.perf_counter()
        build_network(kind, 10000, seed=1, m=2, avg_degree=4)
        build[kind] = time.perf_counter() - t
        print(f"{kind}: {build[kind]:.2f} s", flush=True)

    print("-- time per generation and paper-scale estimate (hours)")
    for kind in ["complete", "single_scale", "scale_free_random", "scale_free"]:
        if kind == "complete":  # N=10,000 complete is too big for the current code; grows with N^2
            cur = per_gen(lambda g: run(kind, 1000, g, seed=1, m=2, avg_degree=4, **ARGS), 5) * 100
        else:
            cur = per_gen(lambda g: run(kind, 10000, g, seed=1, m=2, avg_degree=4, **ARGS), 100) - build[kind] / 100
        vec = per_gen(lambda g: vp.run(kind, 10000, g, seed=1, **ARGS), 500) - build[kind] / 500
        extra = build[kind] * 100 * 25
        print(f"{kind}: current {cur * 1000:.1f} ms/gen -> {(cur * RUNS + extra) / 3600:.0f} h | "
              f"vectorized {vec * 1000:.3f} ms/gen -> {(vec * RUNS + extra) / 3600:.1f} h", flush=True)
