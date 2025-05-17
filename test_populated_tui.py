"""Test TUI with populated data."""

import time
import math
import threading
from clog import ClogTracker


def populate_data(tracker):
    """Populate the tracker with test data."""
    step = 0
    for i in range(100):
        # Log some metrics
        tracker.log_metric("loss", 2.0 * math.exp(-i/20), step)
        tracker.log_metric("accuracy", min(0.99, 0.5 + i/200), step)
        tracker.log_metric("learning_rate", 0.001 * math.exp(-i/50), step)
        
        # Log some messages
        if i % 10 == 0:
            tracker.log(f"Completed iteration {i}")
        if i % 25 == 0:
            tracker.warn(f"Warning at iteration {i}")
        if i == 50:
            tracker.error("Example error at halfway point")
            
        step += 1
        time.sleep(0.1)
    
    tracker.log("Data population complete. Press ESC or 'q' to exit.")


def test_populated_tui():
    """Test the TUI with populated data."""
    tracker = ClogTracker()
    
    # Start populating data in background
    data_thread = threading.Thread(target=populate_data, args=(tracker,))
    data_thread.start()
    
    # Run the UI (blocking)
    tracker.run_ui(threaded=False)
    
    # Wait for data thread to finish
    data_thread.join()


if __name__ == "__main__":
    test_populated_tui()