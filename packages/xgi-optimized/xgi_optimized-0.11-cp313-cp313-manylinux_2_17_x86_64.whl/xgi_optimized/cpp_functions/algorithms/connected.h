#pragma once
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>


bool is_connected(
    const std::unordered_map<int, std::unordered_set<int>>& node_dict,
    const std::unordered_map<int, std::unordered_set<int>>& edge_dict
);
