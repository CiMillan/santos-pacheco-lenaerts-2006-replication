"""Plots named cooperation-fraction-over-generations traces on one panel --
for comparing mechanisms (e.g. imitation vs. swarm) rather than sweeping
T/S like ../../plot.py. Doesn't run any simulation, just visualizes traces
produced elsewhere."""
import matplotlib.pyplot as plt


def plot_traces(traces, title=""):
    """
    traces: {label: trace} where each trace is a list of cooperation
    fractions, one per generation (as returned by average_trace()).
    Returns the Figure.
    """
    fig, ax = plt.subplots()
    for label, trace in traces.items():
        ax.plot(range(len(trace)), trace, label=label)
    ax.set_xlabel("generation")
    ax.set_ylabel("fraction of cooperators")
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.legend()
    return fig
