import csv
import threading
from queue import Queue
from dao import ProductDAO

queue_rows = Queue(maxsize=100)
queue_valid = Queue(maxsize=100)
VALIDATOR_COUNT = 3

class CsvReaderThread(threading.Thread):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        with open(self.file_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                queue_rows.put(row)
        for i in range(VALIDATOR_COUNT):
            queue_rows.put(None)

class ValidationThread(threading.Thread):
    def run(self):
        while True:
            row = queue_rows.get()
            if row is None:
                queue_valid.put(None)
                break
            try:
                name = row[0]
                category = row[1]
                price = float(row[2])
                quantity = int(row[3])
                queue_valid.put((name, category, price, quantity))
            except Exception as e:
                print(f"Invalid row skipped: {row} ({e})")

class DatabaseWriterThread(threading.Thread):
    def __init__(self, progress_bar, total_rows):
        super().__init__()
        self.dao = ProductDAO()
        self.progress_bar = progress_bar
        self.total_rows = total_rows
        self.processed_rows = 0
        self.lock = threading.Lock()

    def run(self):
        finished = 0
        while True:
            item = queue_valid.get()
            if item is None:
                finished += 1
                if finished == VALIDATOR_COUNT:
                    break
                continue
            name, category, price, quantity = item
            self.dao.insert_record(name, category, price, quantity)
            with self.lock:
                self.processed_rows += 1
                self.progress_bar["value"] = self.processed_rows
