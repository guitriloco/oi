#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "wraith_engine.hpp"

namespace py = pybind11;

PYBIND11_MODULE(wraith_core, m) {
    m.doc() = "wraith_core Python bindings";

    py::class_<WraithEngine>(m, "WraithEngine")
        .def(py::init<const std::string&>())
        .def("process_data", &WraithEngine::process_data)
        .def("get_name", &WraithEngine::get_name);
}
