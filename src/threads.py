import csv
import threading
from queue import Queue
from dao import ProductDAO
from error_logger import ErrorLogger
from config import QUEUE_MAXSIZE, VALIDATOR_COUNT, BATCH_SIZE, PROGRESS_UPDATE_INTERVAL


queue_rows = Queue(maxsize=QUEUE_MAXSIZE)
queue_valid = Queue(maxsize=QUEUE_MAXSIZE)


error_logger = ErrorLogger()

class CsvReaderThread(threading.Thread):
    """
    Thread to read CSV file and enqueue rows for validation

    Args:
        file_path (str): Path to the CSV file

    Methods:
        run(): Reads CSV, skips header, enqueues each row to queue_rows
               Puts None for each validator thread to signal end
    """
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        with open(self.file_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                queue_rows.put(row)
        for _ in range(VALIDATOR_COUNT):
            queue_rows.put(None)


class ValidationThread(threading.Thread):
    """
    Thread to validate CSV rows

    Methods:
        run(): Fetches rows from queue_rows, validates and converts data,
               enqueues valid rows to queue_valid. Logs errors if validation fails.
    """
    def run(self):
        while True:
            row = queue_rows.get()
            if row is None:
                queue_valid.put(None)
                break
            try:
                name, category = row[0], row[1]
                price = float(row[2])
                quantity = int(row[3])
                queue_valid.put((name, category, price, quantity))
            except Exception as e:
                error_logger.log(f"Validation error | row={row} | error={e}")


class DatabaseWriterThread(threading.Thread):
    """
    Thread to write validated rows to database in batches

    Args:
        progress_bar: Optional GUI progress bar object.
        total_rows (int): Total number of rows to process

    Methods:
        run(): Fetches validated rows from queue_valid, inserts in batches using ProductDAO,
               updates progress bar, and logs any database errors
    """
    def __init__(self, progress_bar, total_rows):
        super().__init__()
        self.dao = ProductDAO()
        self.progress_bar = progress_bar
        self.total_rows = total_rows
        self.batch_size = BATCH_SIZE
        self.batch = []
        self.processed_rows = 0
        self.finished_validators = 0

    def run(self):
        while True:
            item = queue_valid.get()
            if item is None:
                self.finished_validators += 1
                if self.finished_validators == VALIDATOR_COUNT:
                    break
                continue

            self.batch.append(item)
            self.processed_rows += 1

            if len(self.batch) >= self.batch_size:
                try:
                    self.dao.insert_many(self.batch)
                except Exception as e:
                    error_logger.log(f"DB batch insert error | size={len(self.batch)} | error={e}")
                self.batch.clear()

            if self.progress_bar and self.processed_rows % PROGRESS_UPDATE_INTERVAL == 0:
                self.progress_bar["value"] = self.processed_rows

        if self.batch:
            try:
                self.dao.insert_many(self.batch)
            except Exception as e:
                error_logger.log(f"DB final batch insert error | size={len(self.batch)} | error={e}")
            self.batch.clear()

        if self.progress_bar:
            self.progress_bar["value"] = self.total_rows

