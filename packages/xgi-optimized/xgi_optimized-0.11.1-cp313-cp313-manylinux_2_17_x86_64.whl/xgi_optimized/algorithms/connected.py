"""Algorithms related to connected components of a hypergraph."""
from warnings import warn
from xgi.core.globalviews import subhypergraph
from xgi.exception import XGIError
from .. import cpp_functions

__all__ = [
    "is_connected"
]


def is_connected(H):
    """Optimized is_connected on C++"""
    if H.num_nodes == 0:
        return False

    try:
        return cpp_functions.algorithms.connected.is_connected(H._node, H._edge)
    except Exception as e:
        warn(f"Error in C++ connectivity check: {str(e)}")
        # Fallback to Python implementation
        return len(_plain_bfs(H, list(H.nodes)[0])) == len(H)

