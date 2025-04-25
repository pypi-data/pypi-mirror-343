#include "connected.h"
#include <vector>
#include <cmath>
#include <unordered_map>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <omp.h>

namespace py = pybind11;

void normalize(std::vector<double>& vec) {
    double sum = 0.0;
    #pragma omp parallel for reduction(+:sum)
    for (size_t i = 0; i < vec.size(); ++i) {
        sum += std::abs(vec[i]);
    }
    if (sum == 0.0) return;
    
    const double scale = 1.0 / sum;
    #pragma omp parallel for
    for (size_t i = 0; i < vec.size(); ++i) {
        vec[i] *= scale;
    }
}

std::pair<std::unordered_map<int, double>, std::unordered_map<int, double>>
compute_centralities(
    const std::unordered_map<int, std::unordered_set<int>>& nodes,
    const std::unordered_map<int, std::unordered_set<int>>& edges,
    int max_iter,
    double tol
) {
		omp_set_num_threads(8);
    std::vector<int> node_ids;
    std::vector<int> edge_ids;
    std::unordered_map<int, size_t> node_index;
    std::unordered_map<int, size_t> edge_index;
    std::vector<std::vector<int>> edge_members_list;

    // Заполнение node_ids и node_index
    size_t idx = 0;
    for (const auto& [node_id, _] : nodes) {
        node_ids.push_back(node_id);
        node_index[node_id] = idx++;
    }
    
    // Заполнение edge_ids, edge_index и edge_members_list
    idx = 0;
    for (const auto& [edge_id, members] : edges) {
        edge_ids.push_back(edge_id);
        edge_members_list.push_back(std::vector<int>(members.begin(), members.end()));
        edge_index[edge_id] = idx++;
    }
    
    const size_t num_nodes = node_ids.size();
    const size_t num_edges = edge_ids.size();
    
    std::vector<double> x(num_nodes, 1.0 / num_nodes);
    std::vector<double> y(num_edges, 1.0 / num_edges);
    std::vector<double> new_x(num_nodes);
    std::vector<double> new_y(num_edges);
    std::vector<double> buffer_n(num_nodes);
    std::vector<double> buffer_m(num_edges);

    for (int iter = 0; iter < max_iter; ++iter) {
        // Обновление buffer_n
        std::fill(buffer_n.begin(), buffer_n.end(), 0.0);
        #pragma omp parallel
        {
            std::vector<double> local_buffer_n(num_nodes, 0.0);
            #pragma omp for
            for (size_t i = 0; i < edge_ids.size(); ++i) {
                const size_t edge_idx = i;
                const double y_sq = y[edge_idx] * y[edge_idx];
                for (const auto& node_id : edge_members_list[i]) {
                    const size_t node_idx = node_index.at(node_id);
                    local_buffer_n[node_idx] += y_sq;
                }
            }
            #pragma omp critical
            {
                for (size_t j = 0; j < num_nodes; ++j) {
                    buffer_n[j] += local_buffer_n[j];
                }
            }
        }

        // Обновление new_x
        #pragma omp parallel for
        for (size_t i = 0; i < num_nodes; ++i) {
            new_x[i] = std::sqrt(x[i] * std::sqrt(buffer_n[i]));
        }
        normalize(new_x);

        // Обновление buffer_m
        std::fill(buffer_m.begin(), buffer_m.end(), 0.0);
        #pragma omp parallel for
        for (size_t i = 0; i < edge_ids.size(); ++i) {
            double sum = 0.0;
            for (const auto& node_id : edge_members_list[i]) {
                const size_t node_idx = node_index.at(node_id);
                sum += x[node_idx] * x[node_idx];
            }
            buffer_m[i] = sum;
        }

        // Обновление new_y
        #pragma omp parallel for
        for (size_t j = 0; j < num_edges; ++j) {
            new_y[j] = std::sqrt(y[j] * std::sqrt(buffer_m[j]));
        }
        normalize(new_y);

        // Проверка сходимости
        double diff_nodes = 0.0, diff_edges = 0.0;
        #pragma omp parallel for reduction(+:diff_nodes)
        for (size_t i = 0; i < num_nodes; ++i) {
            diff_nodes += std::abs(new_x[i] - x[i]);
        }
        #pragma omp parallel for reduction(+:diff_edges)
        for (size_t j = 0; j < num_edges; ++j) {
            diff_edges += std::abs(new_y[j] - y[j]);
        }
        double diff = diff_nodes + diff_edges;

        if (diff < tol) {
            x.swap(new_x);
            y.swap(new_y);
            break;
        }
        x.swap(new_x);
        y.swap(new_y);
    }
    std::unordered_map<int, double> node_result, edges_result;
    for (size_t i = 0; i < num_nodes; ++i) {
        node_result[node_ids[i]] = x[i];
    }   
    for (size_t i = 0; i < num_edges; ++i) {
        edges_result[edge_ids[i]] = y[i];
    }

    return std::make_pair(node_result, edges_result);
}
