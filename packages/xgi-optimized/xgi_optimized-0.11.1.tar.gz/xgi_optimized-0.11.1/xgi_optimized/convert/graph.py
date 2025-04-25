"""Method for projecting a hypergraph to a graph."""


import igraph as ig
from xgi.linalg.hypergraph_matrix import adjacency_matrix

__all__ = ["to_ig_graph"]


def to_ig_graph(H):
    """Graph projection (1-skeleton) of the hypergraph H.
    Weights are not considered.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    G : ig.Graph
        The graph projection
    """

    A = adjacency_matrix(H)
    G = ig.Graph.Adjacency(A.toarray().tolist(), mode="undirected")

    node_names = list(H.nodes)
    G.vs["name"] = node_names  # Устанавливаем имена вершин

    return G