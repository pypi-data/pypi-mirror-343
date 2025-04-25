# -----------------------------------------------------------------------------
# src/genome_ninja/_cpp/CMakeLists.txt
# -----------------------------------------------------------------------------

cmake_minimum_required(VERSION 3.18)
project(genome_ninja_cpp LANGUAGES CXX)

include(FetchContent)

find_package(ZLIB QUIET)
if(NOT ZLIB_FOUND)
  message(STATUS "Zlib not found – fetching and building statically")

  FetchContent_Declare(
    zlib
    URL https://github.com/madler/zlib/releases/download/v1.3.1/zlib131.zip
  )
  FetchContent_MakeAvailable(zlib)

  add_library(ZLIB::ZLIB ALIAS zlibstatic)  # 统一风格
endif()

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_fast_reader
    pybind_fast_reader.cpp
    fast_reader.cpp
)

target_compile_features(_fast_reader PRIVATE cxx_std_17)
target_link_libraries(_fast_reader PRIVATE ZLIB::ZLIB)
target_include_directories(_fast_reader PRIVATE ${zlib_SOURCE_DIR})

install(TARGETS _fast_reader DESTINATION genome_ninja)
