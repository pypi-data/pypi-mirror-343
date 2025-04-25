//		omp_set_num_threads(8);
#include "connected.h"
#include <unordered_set>
#include <vector>
#include <algorithm>
#include <omp.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

bool is_connected(
    const std::unordered_map<int, std::unordered_set<int>>& node_dict,
    const std::unordered_map<int, std::unordered_set<int>>& edge_dict
) {
    if (node_dict.empty()) return false;
    
    // 1. Конвертируем node_dict в вектор для параллельной обработки
    std::vector<std::pair<int, std::unordered_set<int>>> node_list(node_dict.begin(), node_dict.end());
    
    // 2. Параллельное построение adjacency list
    std::unordered_map<int, std::vector<int>> adjacency;
    
    #pragma omp parallel
    {
        std::unordered_map<int, std::vector<int>> local_adjacency;
        
        #pragma omp for nowait
        for (size_t idx = 0; idx < node_list.size(); ++idx) {
            const auto& [node_id, edge_set] = node_list[idx];
            for (const auto& edge_id : edge_set) {
                const auto& members = edge_dict.at(edge_id);
                for (const auto& neighbor_id : members) {
                    if (neighbor_id != node_id) {
                        local_adjacency[node_id].push_back(neighbor_id);
                    }
                }
            }
        }
        
        #pragma omp critical
        {
            for (auto& [key, vec] : local_adjacency) {
                adjacency[key].insert(adjacency[key].end(), vec.begin(), vec.end());
            }
        }
    }
    
    // 3. Удаление дубликатов в adjacency
    #pragma omp parallel for
    for (size_t i = 0; i < adjacency.size(); ++i) {
        auto it = std::next(adjacency.begin(), i);
        auto& neighbors = it->second;
        std::sort(neighbors.begin(), neighbors.end());
        auto last = std::unique(neighbors.begin(), neighbors.end());
        neighbors.erase(last, neighbors.end());
    }
    
    // 4. Оптимизированный BFS
    std::unordered_map<int, size_t> node_index;
    std::vector<bool> visited_flag(node_dict.size(), false);
    size_t idx = 0;
    for (const auto& [node_id, _] : node_dict) {
        node_index[node_id] = idx++;
    }
    
    std::vector<int> current_level;
    int start_node = node_dict.begin()->first;
    current_level.push_back(start_node);
    visited_flag[node_index[start_node]] = true;
    
    while (!current_level.empty()) {
        std::vector<int> next_level;
        
        #pragma omp parallel
        {
            std::vector<int> local_next;
            
            #pragma omp for
            for (size_t i = 0; i < current_level.size(); ++i) {
                int current = current_level[i];
                const auto& neighbors = adjacency[current];
                
                for (const auto& neighbor : neighbors) {
                    const size_t neighbor_idx = node_index[neighbor];
                    if (!visited_flag[neighbor_idx]) {
                        #pragma omp critical
                        {
                            if (!visited_flag[neighbor_idx]) {
                                visited_flag[neighbor_idx] = true;
                                local_next.push_back(neighbor);
                            }
                        }
                    }
                }
            }
            
            #pragma omp critical
            next_level.insert(next_level.end(), local_next.begin(), local_next.end());
        }
        
        current_level.swap(next_level);
    }
    
    return std::all_of(visited_flag.begin(), visited_flag.end(), [](bool v) { return v; });
}
