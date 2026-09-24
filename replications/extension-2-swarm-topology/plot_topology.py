"""Draws the topology comparison: one row per network, three columns --
imitation / swarm / swarm minus imitation. The first two columns reuse
../../plot.py's plot_heatmap() unchanged; only the difference column is new."""
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, "../..")
from plot import plot_heatmap


def plot_topology_grid(rows, T_values, S_values, suptitle="", labels=("imitation", "swarm")):
    """
    rows: {network_label: (imitation_results, swarm_results)}, each results
    dict being {(T, S): cooperation_fraction} from sweep() / sweep_swarm().
    Difference column: swarm minus imitation, red-blue colormap fixed at
    -1..+1 so every row uses the same scale (red = swarm cooperates more,
    blue = imitation cooperates more).
    labels: names of the two rules, for the column titles (default
    imitation / swarm; the open-source extension passes its own).
    Returns the Figure.
    """
    fig, axes = plt.subplots(len(rows), 3, figsize=(13, 3.2 * len(rows)), squeeze=False)
    extent = [min(T_values), max(T_values), min(S_values), max(S_values)]

    for i, (label, (imitation, swarm)) in enumerate(rows.items()):
        plot_heatmap(imitation, T_values, S_values, ax=axes[i][0], title=f"{label} -- {labels[0]}")
        plot_heatmap(swarm, T_values, S_values, ax=axes[i][1], title=f"{label} -- {labels[1]}")

        diff = np.array([[swarm[(T, S)] - imitation[(T, S)] for T in T_values] for S in S_values])
        im = axes[i][2].imshow(diff, origin="lower", aspect="auto", cmap="RdBu_r", vmin=-1, vmax=1, extent=extent)
        axes[i][2].set_xlabel("T")
        axes[i][2].set_ylabel("S")
        axes[i][2].set_title(f"{label} -- {labels[1]} minus {labels[0]}")
        plt.colorbar(im, ax=axes[i][2], label="difference")

    fig.suptitle(suptitle)
    fig.tight_layout(rect=[0, 0, 1, 0.97])  # leave room for suptitle
    return fig
