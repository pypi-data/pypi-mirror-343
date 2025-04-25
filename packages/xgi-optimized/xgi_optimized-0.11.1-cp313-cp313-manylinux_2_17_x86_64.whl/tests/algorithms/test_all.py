import numpy as np
import pytest
import random
import xgi
from xgi.exception import XGIError
import xgi_optimized


def test_bipartite_graph():
    H = xgi.load_xgi_data("diseasome")
    g1 = xgi.to_bipartite_graph(H)

    g2 = xgi_optimized.bipartite_graph.to_bipartite_graph(H)
    assert set([n for n in g1.nodes if(g1.nodes[n]["bipartite"]==True)]) == set([n.index for n in g2.vs if(n["type"]==True)])


def test_node_edge_centrality():
    # test empty hypergraph
    H = xgi.Hypergraph()
    assert xgi_optimized.node_edge_centrality(H) == (dict(), dict())

    # Test no edges
    H.add_nodes_from([0, 1, 2])
    nc, ec = xgi_optimized.node_edge_centrality(H)
    assert set(nc) == {0, 1, 2}
    for i in nc:
        assert np.isnan(nc[i])
    assert ec == dict()

    # test disconnected
    H.add_edge([0, 1])
    nc, ec = xgi.node_edge_centrality(H)
    assert set(nc) == {0, 1, 2}
    for i in nc:
        assert np.isnan(nc[i])
    assert set(ec) == {0}
    for i in ec:
        assert np.isnan(ec[i])

    H = xgi.load_xgi_data("email-enron").cleanup()
    assert xgi_optimized.is_connected(H)


def test_line_vector_centrality():
    H = xgi.Hypergraph()
    c = xgi.line_vector_centrality(H)
    assert c == dict()

    with pytest.raises(XGIError):
        H = xgi.Hypergraph()
        H.add_nodes_from([0, 1, 2])
        H.add_edge([0, 1])
        xgi.line_vector_centrality(H)

    H = xgi.sunflower(3, 1, 3) << xgi.sunflower(3, 1, 5)
    c = xgi.line_vector_centrality(H)
    assert len(c[0]) == 4  # sizes 2 through 5
    assert np.allclose(c[0], [0, 0.40824829, 0, 0.24494897])
    assert set(c.keys()) == set(H.nodes)

    with pytest.raises(Exception):
        H = xgi.Hypergraph([["a", "b"], ["b", "c"], ["a", "c"]])
        xgi.line_vector_centrality(H)



@pytest.mark.slow
def test_random_hypergraph_centrality():
    # test empty hypergraph
    H = xgi.Hypergraph()
    H = xgi.fast_random_hypergraph(random.randint(2,50),[0.2,0.1,0.03,0.01])
    print(H.nodes[0])
    assert xgi.is_connected(H) == xgi_optimized.is_connected(H)

def test_improved_node_edge_centrality():
    # test empty hypergraph
    H = xgi.Hypergraph()
    assert xgi_optimized.algorithms.centrality.node_edge_centrality(H) == (dict(), dict())

    # Test no edges
    H.add_nodes_from([0, 1, 2])
    nc, ec =  xgi_optimized.algorithms.centrality.node_edge_centrality(H)
    assert set(nc) == {0, 1, 2}
    for i in nc:
        assert np.isnan(nc[i])
    assert ec == dict()

    H.add_edge([0, 1])
    nc, ec = xgi_optimized.algorithms.centrality.node_edge_centrality(H)
    assert set(nc) == {0, 1, 2}
    for i in nc:
        assert np.isnan(nc[i])
    assert set(ec) == {0}
    for i in ec:
        assert np.isnan(ec[i])
