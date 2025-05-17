"""Test clog without UI to verify imports work."""

from clog import ClogTracker
import time

def main():
    # Create tracker
    tracker = ClogTracker()
    
    # Log some data without starting UI
    print("Created tracker successfully!")
    
    # Log some metrics
    for i in range(5):
        tracker.log_metric("test_metric", i * 1.5, i)
        tracker.log(f"Step {i}")
        print(f"Logged step {i}")
    
    tracker.warn("Test warning")
    tracker.error("Test error")
    
    print("Test completed successfully!")

if __name__ == "__main__":
    main()
