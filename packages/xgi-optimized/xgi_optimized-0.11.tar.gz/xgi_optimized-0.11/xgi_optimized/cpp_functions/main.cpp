#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>  // Required for std::vector conversion
#include "algorithms/centrality.h"
#include "algorithms/connected.h"
#include "convert/line_graph.h"

namespace py = pybind11;

PYBIND11_MODULE(cpp_functions, m) {
		py::module_ m_algorithms = m.def_submodule("algorithms");
		py::module_ m_cetrality = m_algorithms.def_submodule("centrality");
		py::module_ m_connected = m_algorithms.def_submodule("connected");
    m_cetrality.def("compute_centralities", &compute_centralities,
					py::arg("node_dict"),
					py::arg("edge_dict"),
          py::arg("max_iter") = 100,
          py::arg("tol") = 1e-6,
          "Computes node and edge centralities from incidence matrix");
    m_connected.def("is_connected", &is_connected,
          py::arg("node_dict"),
          py::arg("edge_dict"));

		py::module_ m_convert = m.def_submodule("convert");
		py::module_ m_line_graph = m_convert.def_submodule("line_graph");
    m_line_graph.def("compute_line_graph_edges", &compute_line_graph_edges,
        "Compute line graph edges in C++",
        py::arg("hyperedges"),
        py::arg("s"),
        py::arg("weights"),
        py::arg("max_threads"));
}
