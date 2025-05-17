#!/bin/bash

# clog installation script
set -e

echo "================================================="
echo "           Installing clog"
echo "================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "Cargo.toml" ] || [ ! -f "pyproject.toml" ]; then
    echo "Error: Please run this script from the clog directory"
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

# Check for Rust
if ! command -v cargo &> /dev/null; then
    echo "Rust is not installed. Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install maturin
echo "Installing maturin (Rust-Python build tool)..."
pip install maturin

# Build and install clog
echo "Building and installing clog..."
maturin develop --release

echo ""
echo "================================================="
echo "        Installation Complete!"
echo "================================================="
echo ""
echo "To use clog:"
echo "1. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Run the demo:"
echo "   python examples/simple_demo.py"
echo ""
echo "Or use in your Python code:"
echo "   from clog import ClogTracker"
echo "   tracker = ClogTracker()"
echo "   tracker.run_ui(threaded=True)"
echo ""