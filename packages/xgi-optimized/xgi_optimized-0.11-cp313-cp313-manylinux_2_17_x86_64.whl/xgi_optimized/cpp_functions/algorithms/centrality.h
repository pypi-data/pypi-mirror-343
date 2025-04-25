#pragma once
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include <vector>
#include <functional>

namespace py = pybind11;

std::pair<std::unordered_map<int, double>, std::unordered_map<int, double>> 
compute_centralities(
    const std::unordered_map<int, std::unordered_set<int>>& node_dict,
    const std::unordered_map<int, std::unordered_set<int>>& edge_dict,
    int max_iter,
    double tol
);
