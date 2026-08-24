#!/bin/bash
# ============================================================
# Run All Simulations — SKY130 Two-Stage Miller Op-Amp
# ============================================================
# This script runs all testbenches sequentially.
# Requires: ngspice (batch mode)
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_DIR="$PROJECT_ROOT/results"
TESTBENCH_DIR="$PROJECT_ROOT/testbenches"

# Create results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"

echo "================================================"
echo "  SKY130 Two-Stage Miller Op-Amp Simulation"
echo "================================================"
echo ""
echo "Project root: $PROJECT_ROOT"
echo "Results dir:  $RESULTS_DIR"
echo ""

# Check for ngspice
if ! command -v ngspice &> /dev/null; then
    echo "ERROR: ngspice not found in PATH."
    echo "Install with:"
    echo "  Linux:  sudo apt-get install ngspice"
    echo "  macOS:  brew install ngspice"
    echo "  Windows: Use MSYS2: pacman -S mingw-w64-x86_64-ngspice"
    exit 1
fi

echo "ngspice version:"
ngspice --version 2>&1 | head -1
echo ""

# Function to run a testbench
run_tb() {
    local tb_name=$1
    local tb_file="$TESTBENCH_DIR/${tb_name}.spice"
    local log_file="$RESULTS_DIR/${tb_name}.log"
    
    if [ ! -f "$tb_file" ]; then
        echo "WARNING: Testbench not found: $tb_file"
        return 1
    fi
    
    echo "Running: $tb_name"
    echo "  Input:  $tb_file"
    echo "  Output: $log_file"
    
    cd "$PROJECT_ROOT"
    ngspice -b "$tb_file" -o "$log_file" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "  Status: OK"
    else
        echo "  Status: FAILED (exit code $?)"
    fi
    echo ""
}

# Run each testbench
echo "------------------------------------------------"
echo "  Running Testbenches"
echo "------------------------------------------------"
echo ""

run_tb "tb_dc_gain"
run_tb "tb_ac_gain"
run_tb "tb_stability"
run_tb "tb_transient"

echo "================================================"
echo "  All simulations complete."
echo "  Results saved to: $RESULTS_DIR"
echo "================================================"
echo ""
echo "Log files:"
ls -la "$RESULTS_DIR"/*.log 2>/dev/null || echo "  (no log files found)"
echo ""
echo "Data files:"
ls -la "$RESULTS_DIR"/*.txt 2>/dev/null || echo "  (no data files found)"
