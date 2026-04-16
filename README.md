# Supra-Codex Engine

Supra-Codex is a high-performance distributed engine for large-scale data processing and orchestration.

## Directory Structure

- `adapters/`: External system interface adapters.
- `include/`: C++ header files.
- `integrity/`: Data validation and integrity checking modules.
- `models/`: Data models and schemas.
- `orchestration/`: Node management and task scheduling.
- `pipeline/`: Core execution pipelines.
- `src/`: C++ source files and Python bindings.
- `utils/`: Common utilities and logging.
- `tests/`: Unit and integration tests.
- `scripts/`: Maintenance and deployment scripts.

## Build System

The project uses a modern C++/Python build system:
- `scikit-build-core` for build orchestration.
- `pybind11` for C++ to Python bindings.
- `CMake` for C++ build configuration.

### Prerequisites

- Python 3.8+
- CMake 3.15+
- C++17 compiler

### Installation

```bash
pip install .
```

## Quickstart: 3-Node Orchestration

The project includes a master runner that simulates a 3-node distributed environment.

```bash
python run_supra_master.py
```

## Data Contracts

### Task Request
```json
{
  "id": "string",
  "payload": "string",
  "priority": "integer",
  "timestamp": "float"
}
```

### Task Response
```json
{
  "id": "string",
  "node_id": "string",
  "status": "success | error",
  "result": "string",
  "duration": "float"
}
```

## Architecture

The Supra-Codex Engine follows a modular architecture where the high-performance core is implemented in C++ (`wraith_core`) and orchestrated by a Python-based master controller.

1. **WraithEngine (C++)**: Handles heavy computation and data processing.
2. **Master Orchestrator (Python)**: Manages node lifecycle, task distribution, and error recovery.
3. **Integrity Layer**: Ensures data consistency across nodes.
4. **Adapter Layer**: Facilitates communication with various data sources and sinks.
