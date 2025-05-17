"""Test script to verify continuous data generation without UI."""

import time
import threading
import math
import numpy as np
from clog import ClogTracker


def continuous_data_generation(tracker, stop_event):
    """Generate continuous data for the UI to display."""
    step = 0
    epoch = 0
    
    while not stop_event.is_set():
        # Generate simulated metrics with realistic patterns
        batch_loss = 0.5 * math.exp(-step/1000) + np.random.normal(0, 0.02)
        learning_rate = 0.001 * math.exp(-epoch/50)
        
        # Log metrics
        tracker.log_metric("batch_loss", batch_loss, step)
        tracker.log_metric("learning_rate", learning_rate, step // 32)
        
        # Every 32 steps, consider it a new epoch
        if step % 32 == 0:
            epoch_loss = 0.5 * math.exp(-epoch/20) + np.random.normal(0, 0.01)
            tracker.log_metric("epoch_loss", epoch_loss, epoch)
            print(f"Epoch {epoch+1}, Loss: {epoch_loss:.4f}")
            
            # Every 5 epochs, log validation metrics
            if epoch % 5 == 0:
                val_loss = epoch_loss + np.random.uniform(-0.05, 0.1)
                tracker.log_metric("val_loss", val_loss, epoch)
                print(f"Validation loss: {val_loss:.4f}")
            
            epoch += 1
        
        step += 1
        time.sleep(0.05)  # Slower update rate for continuous viewing


def test_continuous_generation():
    """Test continuous data generation without UI."""
    tracker = ClogTracker()
    
    print("Starting continuous data generation test...")
    
    # Start continuous data generation
    stop_event = threading.Event()
    data_thread = threading.Thread(target=continuous_data_generation, args=(tracker, stop_event))
    data_thread.daemon = True
    data_thread.start()
    
    # Run for 5 seconds
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping data generation...")
        stop_event.set()
        data_thread.join(timeout=1)
        print("Test completed.")


if __name__ == "__main__":
    test_continuous_generation()