"""Turns sweep()'s results into contour plots like Fig. 2/3,
Santos, Pacheco & Lenaerts (2006), p. 3491-3492."""
import numpy as np
import matplotlib.pyplot as plt


def plot_heatmap(results, T_values, S_values, ax=None, title=""):
    """
    results: {(T, S): cooperation_fraction} from sweep().
    T_values, S_values: the same lists passed into sweep() -- fixes the
    grid's column/row order, since dict iteration order isn't guaranteed
    to match them.
    ax: an existing matplotlib Axes to draw into, or None to make a new
    figure (useful later for combining several panels side by side, like
    the paper's Left/Right layout).
    Returns the Axes drawn into.
    """
    grid = np.array([[results[(T, S)] for T in T_values] for S in S_values])

    if ax is None:
        _, ax = plt.subplots()

    im = ax.imshow(grid, origin="lower", aspect="auto", cmap="jet", vmin=0, vmax=1,
                    extent=[min(T_values), max(T_values), min(S_values), max(S_values)])
    ax.set_xlabel("T")
    ax.set_ylabel("S")
    ax.set_title(title)
    plt.colorbar(im, ax=ax, label="fraction of cooperators")
    return ax


def plot_pair(results_left, results_right, T_values, S_values,
              title_left="", title_right="", suptitle=""):
    """
    Lays two plot_heatmap() panels side by side, matching how the paper
    presents each figure as a Left/Right pair -- Fig. 2 is complete vs.
    single-scale, Fig. 3 is random scale-free vs. Barabasi-Albert
    scale-free. Each argument pair (results_*, title_*) is one panel.
    Returns the Figure.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    plot_heatmap(results_left, T_values, S_values, ax=axes[0], title=title_left)
    plot_heatmap(results_right, T_values, S_values, ax=axes[1], title=title_right)
    fig.suptitle(suptitle)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    from sweep import sweep

    T_values = [0.5, 1.0, 1.5, 2.0]
    S_values = [-1.0, -0.5, 0.0, 0.5]
    results = sweep("scale_free", n=200, generations=100, T_values=T_values, S_values=S_values,
                     R=1, P=0, num_realizations=10, seed=1, tail=10)

    plot_heatmap(results, T_values, S_values, title="scale-free (demo, n=200)")
    plt.savefig("figures/plot_heatmap_demo.png", dpi=150)
    print("saved figures/plot_heatmap_demo.png")

    results_complete = sweep("complete", n=200, generations=100, T_values=T_values, S_values=S_values,
                              R=1, P=0, num_realizations=10, seed=1, tail=10)
    results_single_scale = sweep("single_scale", n=200, generations=100, T_values=T_values, S_values=S_values,
                                  R=1, P=0, num_realizations=10, seed=1, tail=10)
    plot_pair(results_complete, results_single_scale, T_values, S_values,
              title_left="Complete", title_right="Single-scale",
              suptitle="Evolution of cooperation (demo, n=200) -- cf. Fig. 2")
    plt.savefig("figures/plot_pair_demo.png", dpi=150)
    print("saved figures/plot_pair_demo.png")
