"""Simple test to verify TUI functionality."""

import time
from clog import ClogTracker


def test_tui():
    """Test the TUI with simulated data."""
    tracker = ClogTracker()
    
    # Start the UI
    tracker.run_ui(threaded=False)
    print("TUI started, press ESC or 'q' to exit")


if __name__ == "__main__":
    test_tui()