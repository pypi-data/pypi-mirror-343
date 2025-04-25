"""Methods for converting to and from bipartite graphs."""
import igraph as ig
import networkx as nx

from xgi.core.dihypergraph import DiHypergraph
from xgi.core.hypergraph import Hypergraph
from xgi.exception import XGIError

__all__ = ["from_bipartite_graph", "to_bipartite_graph"]


def from_bipartite_graph(G: ig.Graph, dual=False):
    """
    Create a Hypergraph from a NetworkX bipartite graph.

    Any hypergraph may be represented as a bipartite graph where
    nodes in the first layer are nodes and nodes in the second layer
    are hyperedges.

    The default behavior is to create nodes in the hypergraph
    from the nodes in the bipartite graph where the attribute
    bipartite=0 and hyperedges in the hypergraph from the nodes
    in the bipartite graph with attribute bipartite=1. Setting the
    keyword `dual` reverses this behavior.


    Parameters
    ----------
    G : nx.Graph
        A networkx bipartite graph. Each node in the graph has a property
        'bipartite' taking the value of 0 or 1 indicating the type of node.

    dual : bool, default : False
        If True, get edges from bipartite=0 and nodes from bipartite=1

    Returns
    -------
    Hypergraph or DiHypergraph
        The equivalent hypergraph or directed hypergraph

    References
    ----------
    The Why, How, and When of Representations for Complex Systems,
    Leo Torres, Ann S. Blevins, Danielle Bassett, and Tina Eliassi-Rad,
    https://doi.org/10.1137/20M1355896
    """
    if G.is_directed():
        directed = True
    else:
        directed = False

    edges = []
    nodes = []

    for n in G.vs:
        try:
            node_type = n['type']
        except KeyError as e:
            raise XGIError("bipartite property not set") from e
        if (type(node_type) is bool):
            if node_type:
                edges.append(n.index)
            elif not node_type:
                nodes.append(tuple([n.index, n.attributes()]))

        else:
            raise XGIError("Invalid type specifier")

    if not G.is_bipartite():
        raise XGIError("The network is not bipartite")

    if directed:
        H = DiHypergraph()
    else:
        H = Hypergraph()

    H.add_nodes_from(nodes)

    for e in G.es:
        v = e.target
        u = e.source
        if directed:
            if v in edges:
                H.add_node_to_edge(v, u, direction="in")
            else:
                H.add_node_to_edge(u, v, direction="out")
        else:
            H.add_node_to_edge(v, u)

    return H.dual() if dual else H


def _is_bipartite(G, nodes1, nodes2):
    """Assumption is that nodes1.union(nodes2) == G.nodes"""
    for i, j in G.edges:
        cond1 = i in nodes1
        cond2 = j in nodes2
        if not cond1 == cond2:  # if not both true or both false
            return False
    return True


def to_bipartite_graph(H, index=False):
    if isinstance(H, DiHypergraph):
        directed = True
    else:
        directed = False

    n = H.num_nodes
    m = H.num_edges

    node_dict = dict(zip(H.nodes, range(n)))
    edge_dict = dict(zip(H.edges, range(n, n + m)))

    futurevertexes = [0] * n + [1] * m

    futureedges = set()
    if directed:
        for e in H.edges:
            for v in H.edges.tail(e):
                futureedges.add((node_dict[v], edge_dict[e]))
            for v in H.edges.head(e):
                futureedges.add((edge_dict[e], node_dict[v]))
    else:
        for e in H.edges:
            for v in H.edges.members(e):
                futureedges.add((node_dict[v], edge_dict[e]))

    if directed:
        G = ig.Graph.Bipartite(futurevertexes, list(futureedges), directed=True)

    else:
        G = ig.Graph.Bipartite(futurevertexes, list(futureedges), directed=False)

    phantom_node_id = 0
    for n in H.nodes:
        for k, v in H.nodes[n].items():
            G.vs[phantom_node_id][k] = v
        phantom_node_id += 1

    if index:
        return (
            G,
            {v: k for k, v in node_dict.items()},
            {v: k for k, v in edge_dict.items()},
        )
    else:
        return G
