#include "connected.h"
#include <unordered_set>
#include <queue>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <cmath>
#include <unordered_map>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


namespace py = pybind11;

bool is_connected(
    const std::unordered_map<int, std::unordered_set<int>>& node_dict,
    const std::unordered_map<int, std::unordered_set<int>>& edge_dict
) {
    if (node_dict.empty()) return false;
    
    // Строим отображение: узел -> соседние узлы
    std::unordered_map<int, std::unordered_set<int>> adjacency;
    
    // Сначала строим отображение: ребро -> узлы
    std::unordered_map<int, std::unordered_set<int>> edge_to_nodes;
    for (const auto& [edge_id, node_set] : edge_dict) {
        edge_to_nodes[edge_id] = node_set;
    }
    
    // Затем строим отображение: узел -> соседние узлы через общие ребра
    for (const auto& [node_id, edge_set] : node_dict) {
        for (const auto& edge_id : edge_set) {
            for (const auto& neighbor_id : edge_to_nodes[edge_id]) {
                if (neighbor_id != node_id) {
                    adjacency[node_id].insert(neighbor_id);
                }
            }
        }
    }
    
    // BFS
    std::unordered_set<int> visited;
    std::queue<int> q;
    
    // Начинаем с первого узла
    int start_node = node_dict.begin()->first;
    q.push(start_node);
    visited.insert(start_node);
    
    while (!q.empty()) {
        int current = q.front();
        q.pop();
        
        for (const auto& neighbor : adjacency[current]) {
            if (visited.find(neighbor) == visited.end()) {
                visited.insert(neighbor);
                q.push(neighbor);
            }
        }
    }
    
    return visited.size() == node_dict.size();
}
