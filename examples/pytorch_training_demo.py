"""Demo PyTorch training script with continuous data generation."""

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    PYTORCH_AVAILABLE = True
except ImportError:
    print("PyTorch not available. Will use simulated data instead.")
    PYTORCH_AVAILABLE = False

import numpy as np
import time
import threading
import math
from clog import ClogTracker


def continuous_data_generation(tracker, stop_event):
    """Generate continuous data for the UI to display."""
    step = 0
    epoch = 0
    
    print("Starting continuous data generation...")
    
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
            tracker.log(f"Epoch {epoch+1}, Loss: {epoch_loss:.4f}")
            print(f"Generated: Epoch {epoch+1}, Loss: {epoch_loss:.4f}")
            
            # Every 5 epochs, log validation metrics
            if epoch % 5 == 0:
                val_loss = epoch_loss + np.random.uniform(-0.05, 0.1)
                tracker.log_metric("val_loss", val_loss, epoch)
                tracker.log(f"Validation loss: {val_loss:.4f}")
                print(f"Generated: Validation loss: {val_loss:.4f}")
                
                if val_loss > epoch_loss:
                    tracker.warn("Validation loss is higher than training loss!")
            
            epoch += 1
        
        step += 1
        time.sleep(0.05)  # Slower update rate for continuous viewing


def simulate_training():
    """Simulate training and continuous data generation."""
    # Initialize the tracker
    tracker = ClogTracker()
    
    # Try to start the UI in a separate thread
    try:
        tracker.run_ui(threaded=True)
        ui_started = True
        # Give the UI a moment to start
        time.sleep(0.5)
    except Exception as e:
        print(f"Note: UI could not be started ({e}). Continuing with logging only.")
        ui_started = False
    
    tracker.log("Starting simulated training...")
    print("Starting simulated training...")
    
    # Simulate initial training loop  
    num_epochs = 5  # Reduced for demo
    global_step = 0
    
    for epoch in range(num_epochs):
        epoch_loss = 2.0 * math.exp(-epoch/10)
        
        # Simulate batch training
        for batch_idx in range(32):
            batch_loss = epoch_loss + np.random.normal(0, 0.1)
            
            # Log metrics
            tracker.log_metric("batch_loss", batch_loss, global_step)
            global_step += 1
            
            # Simulate some processing time
            time.sleep(0.01)
        
        # Log epoch metrics
        tracker.log_metric("epoch_loss", epoch_loss, epoch)
        tracker.log_metric("learning_rate", 0.001 * math.exp(-epoch/20), epoch)
        
        # Log messages
        tracker.log(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}")
        print(f"Training: Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}")
        
        # Simulate validation
        if epoch % 5 == 0:
            val_loss = epoch_loss + np.random.uniform(0, 0.2)
            tracker.log_metric("val_loss", val_loss, epoch)
            tracker.log(f"Validation loss: {val_loss:.4f}")
            print(f"Training: Validation loss: {val_loss:.4f}")
            
            if val_loss > epoch_loss:
                tracker.warn("Validation loss is higher than training loss!")
    
    tracker.log("Initial training completed! Continuing with simulated data...")
    print("Initial training completed! Continuing with simulated data...")
    
    # Start continuous data generation
    stop_event = threading.Event()
    data_thread = threading.Thread(target=continuous_data_generation, args=(tracker, stop_event))
    data_thread.daemon = True
    data_thread.start()
    
    # Keep the application running
    if ui_started:
        tracker.log("Press ESC or 'q' in the UI to exit")
        print("UI is running. Press ESC or 'q' in the UI to exit")
    else:
        print("Generating data continuously. Press Ctrl+C to exit")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        stop_event.set()
        data_thread.join(timeout=1)
        print("Stopped.")


if __name__ == "__main__":
    simulate_training()