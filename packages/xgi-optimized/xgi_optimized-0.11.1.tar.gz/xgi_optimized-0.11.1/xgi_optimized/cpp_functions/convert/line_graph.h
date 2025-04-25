#include <unordered_set> 
#include <vector>
#include <tuple>
#include <string>

std::vector<std::tuple<int, int, double>> compute_line_graph_edges(
    const std::vector<std::unordered_set<int>>& hyperedges, 
    int s, 
    const std::string& weights,
    int max_threads = 0
);
