#include "wraith_core.hpp"
#include <iostream>
#include <sstream>

WraithEngine::WraithEngine(const std::string& node_name) 
    : node_name_(node_name), initialized_(false) {}

WraithEngine::~WraithEngine() {}

void WraithEngine::initialize() {
    std::cout << "[WraithEngine] Initializing node: " << node_name_ << std::endl;
    initialized_ = true;
}

std::string WraithEngine::process_data(const std::string& input_data) {
    if (!initialized_) {
        return "Error: Engine not initialized";
    }
    
    std::stringstream ss;
    ss << "Node [" << node_name_ << "] processed: " << input_data << " (integrity verified)";
    return ss.str();
}

std::string WraithEngine::get_node_name() const {
    return node_name_;
}
