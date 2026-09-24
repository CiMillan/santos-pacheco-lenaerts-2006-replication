"""Checks the vectorized prototype gives the same cooperation levels as the
current code (same scale as the reduced-scale figures)."""
import sys
import numpy as np

sys.path.insert(0, "..")
from main import run_batch
import vectorized_prototype as vp


def final(trace):
    return np.mean(trace[-60:])


if __name__ == "__main__":
    for T, S in [(1.5, 0.0), (1.0, 0.5), (1.5, -0.5), (0.5, 0.5)]:
        for kind, n in [("scale_free", 500), ("complete", 200)]:
            loop = [final(t) for t in run_batch(kind, n, 360, 1, S, T, 0, 30, seed=1, m=2, avg_degree=4)]
            vec = [final(vp.run(kind, n, 360, 1, S, T, 0, seed=1 + i)) for i in range(30)]
            se = np.std(loop, ddof=1) / np.sqrt(30)
            print(f"T={T} S={S} {kind}: current {np.mean(loop):.2f} (SE {se:.2f})  vectorized {np.mean(vec):.2f}", flush=True)
