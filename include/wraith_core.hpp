#pragma once

#include <string>
#include <vector>

class WraithEngine {
public:
    WraithEngine(const std::string& node_name);
    ~WraithEngine();

    void initialize();
    std::string process_data(const std::string& input_data);
    std::string get_node_name() const;

private:
    std::string node_name_;
    bool initialized_;
};
