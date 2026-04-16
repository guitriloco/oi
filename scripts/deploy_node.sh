#!/bin/bash

# Supra-Codex Remote Node Deployment Script

set -e

echo "[*] Starting Supra-Codex node deployment..."

# 1. Update and install system dependencies
echo "[*] Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip cmake git build-essential

# 2. Install Python requirements
echo "[*] Installing Python requirements..."
pip3 install requests fastapi uvicorn pydantic

# 3. Clone or setup project directory
if [ ! -d "supra-codex" ]; then
    echo "[*] Cloning repository..."
    # Replace with actual repo URL if needed
    # git clone https://github.com/example/supra-codex.git
    mkdir -p supra-codex
fi

cd supra-codex

# 4. Start the remote agent
echo "[*] Starting remote agent..."
# Ensure the orchestration directory exists if we just created the dir
mkdir -p orchestration
# (In a real scenario, we would have the full code here)

# Example command to run the agent
# python3 orchestration/remote_agent.py --master http://<master-ip>:8000

echo "[+] Deployment complete. Please ensure you have the project files and run orchestration/remote_agent.py"
