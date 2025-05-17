"""Quick test of clog functionality."""

import time
from clog import ClogTracker

def main():
    print("Creating clog tracker...")
    tracker = ClogTracker()
    
    print("Starting UI...")
    tracker.run_ui(threaded=True)
    
    time.sleep(1)
    
    print("Logging some test data...")
    for i in range(20):
        tracker.log_metric("test_metric", i * 0.1, i)
        tracker.log(f"Step {i}")
        time.sleep(0.1)
    
    print("Demo complete! Press 'q' in the UI to quit.")
    tracker.log("Press 'q' to quit")
    
    # Keep running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()