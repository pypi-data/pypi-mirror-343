// -----------------------------------------------------------------------------
// src/genome_ninja/_cpp/pybind_fast_reader.cpp (Python binding)
// -----------------------------------------------------------------------------

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "fast_reader.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_fast_reader, m) {
    m.doc() = "Blazing‑fast *.fna.gz byte counter (C++17)";
    m.def("uncompressed_bytes", &uncompressed_bytes,
          py::arg("paths"), py::arg("threads") = 8);
}
