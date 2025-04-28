import sys
import time
import threading

class Animation:
    """Class to show loading animation while processing is happening"""
    
    def __init__(self):
        self.running = False
        self._stop_event = threading.Event()  # Use Event for proper thread signaling
    
    def start(self, text="Processing..."):
        """Start the animation"""
        self.running = True
        self._stop_event.clear()  # Clear any previous stop signal
        
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        
        # Print initial animation frame
        sys.stdout.write(f"\r{spinner[i]} {text}")
        sys.stdout.flush()
        
        while not self._stop_event.is_set():
            i = (i + 1) % len(spinner)
            # Clear the current line with ANSI escape code
            sys.stdout.write("\r\033[K")  # Clear line from cursor to end
            sys.stdout.write(f"{spinner[i]} {text}")
            sys.stdout.flush()
            self._stop_event.wait(0.1)  # Wait with timeout to check for stop event
        
        # Clear the animation line when done
        sys.stdout.write("\r\033[K")  # Clear the line
        sys.stdout.flush()
    
    def stop(self):
        """Stop the animation and force clear the line"""
        self._stop_event.set()  # Signal thread to stop
        self.running = False
        
        # Force clear the line immediately from this thread
        # This ensures the line is cleared even if the animation thread hasn't noticed the stop signal yet
        time.sleep(0.1)  # Give a small pause to ensure thread has time to process
        sys.stdout.write("\r\033[K")  # Clear line from cursor to end
        sys.stdout.write("\r")        # Move cursor to beginning of line
        sys.stdout.flush()
        
        # Print a newline to ensure the next output starts on a fresh line
        # sys.stdout.write("\n")
        sys.stdout.flush()