cmake_minimum_required(VERSION 3.15)
project(oi VERSION 0.1.0)

find_package(pybind11 REQUIRED)

include_directories(include)

pybind11_add_module(wraith_core src/main.cpp src/wraith_engine.cpp)

install(TARGETS wraith_core DESTINATION .)
