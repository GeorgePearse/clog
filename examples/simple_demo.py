"""Simple demo of clog without PyTorch dependency."""

import time
import math
import random
from clog import ClogTracker


def main():
    """Run a simple demo of clog functionality."""
    # Initialize the tracker
    tracker = ClogTracker()
    
    # Start the UI
    tracker.run_ui(threaded=True)
    
    # Give the UI a moment to start
    time.sleep(0.5)
    
    tracker.log("Starting simple demo...")
    
    # Simulate training metrics
    for step in range(200):
        # Generate some synthetic metrics
        loss = 5.0 * math.exp(-step / 50.0) + random.gauss(0, 0.1)
        accuracy = min(0.99, step / 200.0 + random.gauss(0, 0.02))
        learning_rate = 0.001 * (0.9 ** (step // 20))
        
        # Log metrics
        tracker.log_metric("loss", loss, step)
        tracker.log_metric("accuracy", accuracy, step)
        tracker.log_metric("learning_rate", learning_rate, step)
        
        # Add some messages
        if step % 10 == 0:
            tracker.log(f"Step {step}: loss={loss:.4f}, acc={accuracy:.4f}")
        
        if step % 30 == 0 and step > 0:
            tracker.warn(f"Checkpoint at step {step}")
        
        if accuracy > 0.9 and step == 150:
            tracker.log("Reached 90% accuracy!")
        
        # Sleep to simulate processing
        time.sleep(0.05)
    
    tracker.log("Demo completed!")
    tracker.error("Example error: This is what errors look like")
    
    # Keep running so user can interact with UI
    tracker.log("Use arrow keys to navigate metrics")
    tracker.log("Press '/' to search for metrics") 
    tracker.log("Press 'q' to quit")
    
    # Keep the UI running
    time.sleep(60)


if __name__ == "__main__":
    main()