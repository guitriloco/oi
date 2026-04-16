# Supra-Codex Engine

## Overview
The Supra-Codex Engine is a modular, high-performance orchestration framework designed for distributed data processing and integrity verification.

## Directory Structure
- `pipeline/`: Data ingestion and transformation pipelines.
- `integrity/`: Cryptographic and logical integrity checks.
- `orchestration/`: Node management and task dispatching.
- `adapters/`: Connectivity to external data sources and sinks.
- `models/`: Data models and schema definitions.
- `utils/`: Common utility functions.
- `src/`: C++ source files for `wraith_core`.
- `include/`: C++ header files.
- `tests/`: Unit and integration tests.
- `scripts/`: Maintenance and deployment scripts.

## Build Instructions

### Prerequisites
- CMake (>= 3.15)
- C++17 Compiler
- Python (>= 3.7)
- `pip install scikit-build-core pybind11`

### Installation
To build and install the `wraith_core` module:
```bash
pip install .
```

Alternatively, for development:
```bash
pip install -e .
```

## Quickstart: 3-Node Orchestration
The master runner simulates a 3-node environment locally.

1. Build the project (see above).
2. Run the master orchestrator:
```bash
python run_supra_master.py
```

## Data Contracts
The engine uses the following preliminary data contracts:

### Node Payload
| Field | Type | Description |
|-------|------|-------------|
| `instruction` | String | The task command for the node |
| `integrity_hash`| String | SHA-256 hash for verification |

### Node Result
| Field | Type | Description |
|-------|------|-------------|
| `status` | String | SUCCESS or FAILURE |
| `output` | String | Processed data or error message |
| `node_id`| String | Identity of the processing node |
