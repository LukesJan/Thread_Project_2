import threading
from datetime import datetime
from config import ERROR_LOG_FILE

class ErrorLogger:
    def __init__(self):
        """
        Initialize the ErrorLogger

        - Sets the log file path from ERROR_LOG_FILE
        - Creates a threading.Lock to ensure thread-safe logging
        """
        self.file_path = ERROR_LOG_FILE
        self.lock = threading.Lock()

    def log(self, message: str):
        """
        Append a timestamped error message to the log file

        - Thread-safe: acquires a lock before writing

        Args:
            message (str): The error message to log
        """
        with self.lock:
            with open(self.file_path, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {message}\n")
