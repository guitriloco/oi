cmake_minimum_required(VERSION 3.15)
project(wraith_core VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

pybind11_add_module(wraith_core
    src/wraith_core.cpp
    src/bindings.cpp
)

target_include_directories(wraith_core PRIVATE include)

install(TARGETS wraith_core DESTINATION .)
