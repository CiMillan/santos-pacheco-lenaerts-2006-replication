"""The real network: the giant component of the foundation-model supply chain,
from the Ecosystem Graphs release (Bommasani et al., 2024) as packaged in
fm-networks-labs. The data stays there and is not copied into this repo."""
import os
from pathlib import Path

import networkx as nx
import pandas as pd

FM_DATA = Path(os.environ.get(
    "FM_DATA", Path.home() / "Desktop/fm-networks-labs/dist/student-kit/data/fm-2024-05-d3c06a4"))


def load_fm_giant(data_dir=FM_DATA):
    """
    Returns the giant component as an undirected simple graph with nodes
    0..n-1 (assets sorted by name, so the numbering is fixed). Each node keeps
    its asset "name" and "type" (dataset, model, application).
    Undirected: in the game both ends of a dependency play each other and see
    each other's payoff (design choice, no source). Self-loops and repeated
    edges are dropped.
    """
    nodes = pd.read_csv(Path(data_dir) / "nodes.csv")
    edges = pd.read_csv(Path(data_dir) / "edges.csv")
    g = nx.Graph()
    for row in nodes.itertuples():
        g.add_node(row.name, type=row.type)
    g.add_edges_from((u, v) for u, v in zip(edges.upstream, edges.downstream) if u != v)
    giant = g.subgraph(max(nx.connected_components(g), key=len))
    names = sorted(giant.nodes)
    out = nx.Graph()
    for i, name in enumerate(names):
        out.add_node(i, name=name, type=giant.nodes[name].get("type"))
    index = {name: i for i, name in enumerate(names)}
    out.add_edges_from((index[u], index[v]) for u, v in giant.edges)
    return out


def rewire_keep_degrees(graph, seed):
    """
    Null model: the same nodes and degrees, links shuffled at random by
    repeated edge swaps -- the same washing-out the paper uses for its
    scale_free_random network (../../network.py). Separates "sparse, few
    hubs" from "the real wiring". Node attributes are kept.
    """
    g = graph.copy()
    nx.double_edge_swap(g, nswap=10 * g.number_of_edges(), max_tries=100 * g.number_of_edges(), seed=seed)
    return g
