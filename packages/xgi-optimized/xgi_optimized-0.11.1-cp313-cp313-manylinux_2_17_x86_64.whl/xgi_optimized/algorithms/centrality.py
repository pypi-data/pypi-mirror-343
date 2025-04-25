"""Algorithms for computing the centralities of nodes (and edges) in a hypergraph."""

from warnings import warn

import networkx as nx
import numpy as np
from numpy.linalg import norm
from scipy.sparse.linalg import eigsh

from ..cpp_functions.algorithms.centrality import compute_centralities
from xgi.exception import XGIError
from ..algorithms.connected import is_connected

__all__ = [
    "node_edge_centrality"
]


def node_edge_centrality(
    H,
    max_iter=100,
    tol=1e-6,
):
    """Optimized version node-edge centrality on C++"""
    if H.num_nodes == 0 or H.num_edges == 0 or not is_connected(H):
        return {n: np.nan for n in H.nodes}, {e: np.nan for e in H.edges}

    # Вызываем C++ функцию
    try:
        node_result, edge_result = compute_centralities(
            H._node,
            H._edge,
            max_iter,
            tol
        )
    except Exception as e:
        warn(f"Error in C++ computation: {str(e)}")
        return {n: np.nan for n in H.nodes}, {e: np.nan for e in H.edges}

    return node_result, edge_result

