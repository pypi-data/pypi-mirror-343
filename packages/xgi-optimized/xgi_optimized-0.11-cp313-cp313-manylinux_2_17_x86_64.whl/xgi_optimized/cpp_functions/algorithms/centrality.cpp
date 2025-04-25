#include "connected.h"
#include <vector>
#include <cmath>
#include <unordered_map>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

void normalize(std::vector<double>& vec) {
    double sum = 0.0;
    for (const auto& val : vec) {
        sum += std::abs(val);
    }
    if (sum == 0.0) return;
    
    const double scale = 1.0 / sum;
    for (auto& val : vec) {
        val *= scale;
    }
}

std::pair<std::unordered_map<int, double>, std::unordered_map<int, double>>
compute_centralities(
    const std::unordered_map<int, std::unordered_set<int>>& nodes,
    const std::unordered_map<int, std::unordered_set<int>>& edges,
    int max_iter,
    double tol
) {
    // Создаем mapping узлов и ребер
    std::vector<int> node_ids;
    std::vector<int> edge_ids;
    std::unordered_map<int, size_t> node_index;
    std::unordered_map<int, size_t> edge_index;
    
    // Заполняем индексы узлов
    size_t idx = 0;
    for (const auto& [node_id, _] : nodes) {
        node_ids.push_back(node_id);
        node_index[node_id] = idx++;
    }
    
    // Заполняем индексы ребер
    idx = 0;
    for (const auto& [edge_id, _] : edges) {
        edge_ids.push_back(edge_id);
        edge_index[edge_id] = idx++;
    }
    
    const size_t num_nodes = node_ids.size();
    const size_t num_edges = edge_ids.size();
    
    // Инициализируем векторы центральностей
    std::vector<double> x(num_nodes, 1.0 / num_nodes);
    std::vector<double> y(num_edges, 1.0 / num_edges);
    std::vector<double> new_x(num_nodes);
    std::vector<double> new_y(num_edges);
    std::vector<double> buffer_n(num_nodes);
    std::vector<double> buffer_m(num_edges);

    // Основной алгоритм
    for (int iter = 0; iter < max_iter; ++iter) {
        // Вычисляем I @ (y^2)
        std::fill(buffer_n.begin(), buffer_n.end(), 0.0);
        for (const auto& [edge_id, edge_members] : edges) {
            const size_t edge_idx = edge_index[edge_id];
            const double y_sq = y[edge_idx] * y[edge_idx];
            
            for (const auto& node_id : edge_members) {
                const size_t node_idx = node_index[node_id];
                buffer_n[node_idx] += y_sq;
            }
        }

        // Вычисляем new_x = sqrt(x * sqrt(I @ y^2))
        for (size_t i = 0; i < num_nodes; ++i) {
            new_x[i] = std::sqrt(x[i] * std::sqrt(buffer_n[i]));
        }
        normalize(new_x);

        // Вычисляем I.T @ (x^2)
        std::fill(buffer_m.begin(), buffer_m.end(), 0.0);
        for (const auto& [edge_id, edge_members] : edges) {
            const size_t edge_idx = edge_index[edge_id];
            
            for (const auto& node_id : edge_members) {
                const size_t node_idx = node_index[node_id];
                buffer_m[edge_idx] += x[node_idx] * x[node_idx];
            }
        }

        // Вычисляем new_y = sqrt(y * sqrt(I.T @ x^2))
        for (size_t j = 0; j < num_edges; ++j) {
            new_y[j] = std::sqrt(y[j] * std::sqrt(buffer_m[j]));
        }
        normalize(new_y);

        // Проверка сходимости
        double diff = 0.0;
        for (size_t i = 0; i < num_nodes; ++i) {
            diff += std::abs(new_x[i] - x[i]);
        }
        for (size_t j = 0; j < num_edges; ++j) {
            diff += std::abs(new_y[j] - y[j]);
        }

        if (diff < tol) {
				x = new_x;
		        y = new_y;
				break;
        }

        x = new_x;
        y = new_y;
    }
		std::unordered_map<int, double> node_result;
		std::unordered_map<int, double> edges_result;
		for (size_t i = 0; i < num_nodes; i++) 
			node_result[node_ids[i]] = x[i];
		
		for (size_t i = 0; i < num_edges; i++) 
			edges_result[edge_ids[i]] = y[i];
		
		return std::make_pair(node_result, edges_result);
}
