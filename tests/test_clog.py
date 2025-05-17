"""Tests for clog."""

import pytest
import time
from clog import ClogTracker


def test_tracker_creation():
    """Test that we can create a tracker."""
    tracker = ClogTracker()
    assert tracker is not None


def test_log_metric():
    """Test logging metrics."""
    tracker = ClogTracker()
    
    # Should not raise any exception
    tracker.log_metric("test_metric", 1.0, 0)
    tracker.log_metric("test_metric", 2.0, 1)
    tracker.log_metric("another_metric", 3.0, 0)


def test_log_messages():
    """Test logging messages."""
    tracker = ClogTracker()
    
    # Should not raise any exception
    tracker.log("Info message")
    tracker.warn("Warning message")
    tracker.error("Error message")
    tracker.log_message("Custom", "info")


def test_ui_starts_and_stops():
    """Test that UI can start and stop."""
    tracker = ClogTracker()
    
    # Start UI in thread
    tracker.run_ui(threaded=True)
    
    # Give it a moment
    time.sleep(0.5)
    
    # Should still be able to log
    tracker.log_metric("test", 1.0, 0)
    tracker.log("Test message")
    
    # Stop the UI thread (in the future we'd have a proper stop method)
    tracker.stop_ui()