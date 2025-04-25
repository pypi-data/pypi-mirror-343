### What has been done?: ###
- [Metrics computation has been updated](#updated-metrics-calculation)
- [The implementation of bipartite graphs has been changed](#getting-started)
- [Application of graph and hypergraph metrics to improve ML models](#graph-usage)
- [Cpp implementation of linegraph](#cpp-imp)


## Metrics computation has been updated<a id="updated-metrics-calculation"></a>

The computation of the linegraph vector centrality metric was accelerated by using the igraph library instead of networkx . For comparison, implementations using the networkx.Graph class were retained.
```python
H_enron = xgi.load_xgi_data("plant-pollinator-mpl-034")
H_enron_cleaned = H_enron.cleanup(
    multiedges=False, singletons=False, isolates=False, relabel=True, in_place=False
)
start_time = time.time()

xgi.centrality.line_vector_centrality(H_enron_cleaned)

middle_time = time.time()

xgi.centrality.fast_line_vector_centrality(H_enron_cleaned)

end_time = time.time()

print(f"Время выполнения nx: {(middle_time-start_time):.6f} секунд")
print(f"Время выполнения ig: {(end_time-middle_time):.6f} секунд")
```

## The implementation of bipartite graphs has been changed. <a id="getting-started"></a>
The implementation for working with bipartite graphs was modified: the igraph.Graph class is 
now used instead of networkx.Graph for converting from a Hypergraph to a bipartite graph and back to a Hypergraph .
```python
hg = xgi.Hypergraph()
hg.add_edges_from(
    [[1, 2, 3], [3, 4, 5,8], [1, 4, 10, 11, 12], [7,0,8], [5,7,2]]
)

bpg = xgi.convert.to_bipartite_graph(hg)
plot(bpg,vertex_label=bpg.vs.indices,layout = Graph.layout_bipartite(bpg), bbox=(0, 0, 500,500))
```

## Application of graph and hypergraph metrics to improve ML models<a id="graph-usage"></a> 
[In the file](https://github.com/Samoylo57/iHyperGraph/blob/Matvei/OGBN-MAG/ogbn-mag.ipynb)
 for solving the classification problem, in addition to 
article embeddings, article identifiers, and author IDs used as features, 
metrics such as eigenvector centrality of the graph and vector centrality of 
the hypergraph were also utilized.

## Cpp implementation of linegraph<a id="cpp-imp"></a>
* **In progress...**
