"""Parameter sweep -- reproduces the shape of Fig. 2/3's (T, S) heatmaps,
Santos, Pacheco & Lenaerts (2006), p. 3491-3492. Built on top of main.py's
run_batch(); doesn't change the core loop, just calls it at every grid point."""
from main import run_batch, average_trace


def sweep(network_kind, n, generations, T_values, S_values, R, P, num_realizations, seed,
          initial_c_fraction=0.5, m=4, tail=20):
    """
    Runs run_batch() at every (T, S) combination in the grid.
    tail: average the last `tail` generations of the averaged trace, not
    just the final generation -- finite populations keep fluctuating even
    once "converged," so a single last point is noisier than it needs to be.
    Returns {(T, S): average cooperation fraction}.
    """
    results = {}
    for T in T_values:
        for S in S_values:
            traces = run_batch(network_kind, n, generations, R, S, T, P,
                                num_realizations, seed, initial_c_fraction, m)
            avg = average_trace(traces)
            results[(T, S)] = sum(avg[-tail:]) / tail
    return results


if __name__ == "__main__":
    import time

    T_values = [0.5, 1.0, 1.5, 2.0]
    S_values = [-1.0, -0.5, 0.0, 0.5]
    start = time.time()
    results = sweep("scale_free", n=200, generations=100, T_values=T_values, S_values=S_values,
                     R=1, P=0, num_realizations=10, seed=1, tail=10)
    print(f"grid: {len(T_values)}x{len(S_values)} points, took {time.time() - start:.1f}s\n")
    print("S \\ T  " + "  ".join(f"{t:5.1f}" for t in T_values))
    for S in S_values:
        row = "  ".join(f"{results[(T, S)]:5.2f}" for T in T_values)
        print(f"{S:5.1f}  {row}")
