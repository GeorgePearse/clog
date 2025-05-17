"""Terminal-based training logger for PyTorch models."""

from ._rust import ClogTracker as _ClogTracker
from typing import Optional, Union
import threading


class ClogTracker:
    """Main tracker for logging metrics and messages during training."""
    
    def __init__(self):
        self._tracker = _ClogTracker()
        self._ui_thread = None
    
    def log_metric(self, name: str, value: float, step: int) -> None:
        """Log a metric value."""
        self._tracker.log_metric(name, value, step)
    
    def log_message(self, message: str, level: str = "info") -> None:
        """Log a message at the specified level."""
        self._tracker.log_message(message, level)
    
    def log(self, message: str) -> None:
        """Log an info message."""
        self.log_message(message, "info")
    
    def warn(self, message: str) -> None:
        """Log a warning message."""
        self.log_message(message, "warning")
    
    def error(self, message: str) -> None:
        """Log an error message."""
        self.log_message(message, "error")
    
    def run_ui(self, threaded: bool = True) -> None:
        """Run the terminal UI."""
        if threaded:
            self._ui_thread = threading.Thread(target=self._tracker.run_ui)
            self._ui_thread.daemon = True
            self._ui_thread.start()
        else:
            self._tracker.run_ui()
    
    def stop_ui(self) -> None:
        """Stop the UI if running in a thread."""
        if self._ui_thread and self._ui_thread.is_alive():
            # Note: This doesn't actually stop the thread gracefully
            # In production you'd want a better shutdown mechanism
            pass


__all__ = ["ClogTracker"]