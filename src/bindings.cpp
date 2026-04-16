#include <pybind11/pybind11.h>
#include "wraith_core.hpp"

namespace py = pybind11;

PYBIND11_MODULE(wraith_core, m) {
    m.doc() = "wraith_core Python bindings";

    py::class_<WraithEngine>(m, "WraithEngine")
        .def(py::init<const std::string&>())
        .def("initialize", &WraithEngine::initialize)
        .def("process_data", &WraithEngine::process_data)
        .def("get_node_name", &WraithEngine::get_node_name);
}
