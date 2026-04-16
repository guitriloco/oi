#pragma once
#include <string>
#include <vector>

class WraithEngine {
public:
    WraithEngine(const std::string& name);
    std::string process_data(const std::string& input);
    std::string get_name() const;

private:
    std::string name_;
};
