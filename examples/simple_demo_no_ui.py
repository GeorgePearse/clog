"""Simple demo of clog without UI for environments that don't support terminal UI."""

import time
import math
import random
from clog import ClogTracker


def main():
    """Run a simple demo of clog functionality."""
    # Initialize the tracker
    tracker = ClogTracker()
    
    # Skip UI in non-terminal environments
    print("Starting clog demo (without UI)...")
    
    tracker.log("Starting simple demo...")
    
    # Simulate training metrics
    for step in range(50):  # Reduced steps for demo
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
            print(f"Step {step}: loss={loss:.4f}, acc={accuracy:.4f}")
        
        if step % 30 == 0 and step > 0:
            tracker.warn(f"Checkpoint at step {step}")
        
        if accuracy > 0.9 and step == 40:
            tracker.log("Reached 90% accuracy!")
        
        # Sleep to simulate processing
        time.sleep(0.01)
    
    tracker.log("Demo completed!")
    tracker.error("Example error: This is what errors look like")
    
    print("Demo completed successfully!")
    print("Metrics and logs have been tracked by clog.")


if __name__ == "__main__":
    main()
