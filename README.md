# clog - Terminal UI Logger for Model Training

clog is a terminal-based logging and monitoring tool for machine learning model training, written in Rust with Python bindings. It provides a TensorBoard-like experience directly in your terminal.

## Features

- **Live Metrics Visualization**: Real-time graphs of training metrics
- **Interactive UI**: Navigate between metrics with arrow keys
- **Search Functionality**: Filter metrics by name with `/`
- **Colored Logs**: Different colors for info, warning, and error messages
- **Thread-safe**: Can be used from multiple threads safely
- **Fast**: Built with Rust for performance

## Installation

### Quick Install (Easiest)

```bash
# Clone the repository
git clone https://github.com/yourusername/clog.git
cd clog

# Run the install script
./install.sh

# Activate the virtual environment
source .venv/bin/activate

# Test it out
python examples/simple_demo.py
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## Usage

### Basic Example

```python
from clog import ClogTracker
import time

# Create a tracker
tracker = ClogTracker()

# Start the UI in a separate thread
tracker.run_ui(threaded=True)

# Log metrics
for step in range(100):
    tracker.log_metric("loss", 1.0 / (step + 1), step)
    tracker.log_metric("accuracy", step / 100.0, step)
    
    if step % 10 == 0:
        tracker.log(f"Step {step} completed")
    
    time.sleep(0.1)

# Keep UI running
time.sleep(30)
```

### PyTorch Integration

```python
import torch
from clog import ClogTracker

tracker = ClogTracker()
tracker.run_ui(threaded=True)

# In your training loop
for epoch in range(num_epochs):
    for batch_idx, (data, target) in enumerate(dataloader):
        # ... training code ...
        
        tracker.log_metric("batch_loss", loss.item(), global_step)
        
    tracker.log_metric("epoch_loss", epoch_loss, epoch)
    tracker.log(f"Epoch {epoch} completed")
```

## UI Controls

- **Arrow Keys**: Navigate between metrics (up/down)
- **`/`**: Enter search mode to filter metrics
- **`Enter`/`Esc`**: Exit search mode
- **`q`**: Quit the application

## Development

```bash
# Install development dependencies
uv add --dev pytest ruff mypy maturin

# Run tests
pytest

# Run linters
ruff check .
mypy .

# Build the Rust extension
maturin develop
```

## Architecture

clog consists of:
- Rust backend using `ratatui` for terminal UI
- Python bindings via `PyO3`
- Thread-safe metric storage
- Real-time chart rendering

## License

MIT