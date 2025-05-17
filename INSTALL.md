# Installation Guide for clog

## Quick Install (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd clog

# Run the install script
./install.sh

# Activate the virtual environment
source .venv/bin/activate

# Run the demo
python examples/simple_demo.py
```

## Manual Installation

### Prerequisites

1. **Python 3.8+**
2. **Rust toolchain**

If you don't have Rust:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Steps

1. **Create and activate a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install maturin (build tool):**
```bash
pip install maturin
```

3. **Build and install clog:**
```bash
maturin develop --release
```

## Verify Installation

```python
# Test that it works
python -c "from clog import ClogTracker; print('clog installed successfully!')"
```

## Run the Demo

```bash
# Simple demo without PyTorch
python examples/simple_demo.py

# PyTorch example (requires PyTorch)
pip install torch
python examples/pytorch_training.py
```

## Troubleshooting

### "Module not found" error
- Make sure you activated the virtual environment
- Run `maturin develop` again

### Rust compilation errors
- Update Rust: `rustup update`
- Make sure you have a C compiler installed

### Python linking errors
- On Ubuntu/Debian: `sudo apt install python3-dev`
- On macOS: Install Xcode command line tools