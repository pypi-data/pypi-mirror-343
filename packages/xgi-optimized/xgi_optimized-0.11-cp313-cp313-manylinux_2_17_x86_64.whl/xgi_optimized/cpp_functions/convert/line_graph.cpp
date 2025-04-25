// Made by TimurPshITMO
#include "line_graph.h"
#include <vector>
#include <unordered_set>
#include <tuple>
#include <string>
#include <omp.h>

std::vector<std::tuple<int, int, double>> compute_line_graph_edges(
    const std::vector<std::unordered_set<int>>& hyperedges, 
    int s, 
    const std::string& weights,
    int max_threads) { // Новый аргумент для управления количеством потоков

    std::vector<std::tuple<int, int, double>> edges;
    int n = hyperedges.size();

    // Устанавливаем количество потоков
    if (max_threads > 0) {
        omp_set_num_threads(max_threads); // Используем указанное количество потоков
    }

    #pragma omp parallel for schedule(static)
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            std::unordered_set<int> intersection;
            for (const auto& elem : hyperedges[i]) {
                if (hyperedges[j].count(elem)) {
                    intersection.insert(elem);
                }
            }

            if (intersection.size() >= s) {
                double weight = 0.0;
                if (weights == "absolute") {
                    weight = intersection.size();
                } else if (weights == "normalized") {
                    weight = static_cast<double>(intersection.size()) /
                             std::min(hyperedges[i].size(), hyperedges[j].size());
                }

                #pragma omp critical
                edges.emplace_back(i, j, weight);
            }
        }
    }

    return edges;
}
