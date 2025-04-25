### What has been done?: ###
- [Metrics computation has been updated](#updated-metrics-calculation)
- [The implementation of bipartite graphs has been changed](#getting-started)
- [Cpp implementation of linegraph](#cpp-imp)
- [Added the ability to use the package of accelerated functions on hypergraphs](#pip)

## Metrics computation has been updated<a id="updated-metrics-calculation"></a>

The computation of the linegraph vector centrality metric was accelerated by using the с++ instead of python. For comparison, implementations using the networkx.Graph class were retained.
```python
H_enron = xgi.load_xgi_data("plant-pollinator-mpl-034")
H_enron_cleaned = H_enron.cleanup(
    multiedges=False, singletons=False, isolates=False, relabel=True, in_place=False
)
start_time = time.time()

xgi.centrality.line_vector_centrality(H_enron_cleaned)

middle_time = time.time()

xgi_optimized.vector_centrality(H_enron_cleaned, 3)

end_time = time.time()

print(f"Время выполнения python: {(middle_time-start_time):.6f} секунд")
print(f"Время выполнения c++: {(end_time-middle_time):.6f} секунд")
```

## The implementation of bipartite graphs has been changed. <a id="getting-started"></a>
The implementation for working with bipartite graphs was modified: the igraph.Graph class is 
now used instead of networkx.Graph for converting from a Hypergraph to a bipartite graph and back to a Hypergraph .
```python
hg = xgi.Hypergraph()
hg.add_edges_from(
    [[1, 2, 3], [3, 4, 5,8], [1, 4, 10, 11, 12], [7,0,8], [5,7,2]]
)

bpg = xgi_optimized.biparite_graph.to_bipartite_graph(hg)
```

## Cpp implementation of сhecking graph connectivity<a id="cpp-imp"></a>
```python
size = 38
hg = xgi.fast_random_hypergraph(size,[0.1, 0.2, 0.02,0.04])
start_time = time.time() 
xgi_optimized.connected.is_connected(hg)
middle_time = time.time()
xgi.centrality.is_connected(hg)
end_time = time.time()
print(f"Время выполнения c++: {(middle_time-start_time):.6f} секунд")
print(f"Время выполнения python: {(end_time-middle_time):.6f} секунд")
```
## Cpp implementation of сhecking graph connectivity<a id="cpp-imp"></a>
```python
size = 38
hg = xgi.fast_random_hypergraph(size,[0.1, 0.2, 0.02,0.04])
start_time = time.time() 
xgi_optimized.connected.is_connected(hg)
middle_time = time.time()
xgi.centrality.is_connected(hg)
end_time = time.time()
print(f"Время выполнения c++: {(middle_time-start_time):.6f} секунд")
print(f"Время выполнения python: {(end_time-middle_time):.6f} секунд")
```
## Added the ability to use the package of accelerated functions on hypergraphs<a id="cpp-imp"></a>
```bash
pip install xgi_optimized
```
