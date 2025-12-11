import json
import sys
import os

if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(base_path, "config.json")

with open(config_path, "r", encoding="utf-8") as f:
    """
    Loads config from file.
    """
    cfg = json.load(f)


CSV_FILE = cfg.get("csv_file", "data.csv")
ERROR_LOG_FILE = cfg.get("error_log_file", "error.log")


BATCH_SIZE = cfg.get("batch_size", 500)
QUEUE_MAXSIZE = cfg.get("queue_maxsize", 5000)
VALIDATOR_COUNT = cfg.get("validator_count", 12)
PROGRESS_UPDATE_INTERVAL = cfg.get("progress_update_interval", 200)
RATE_LIMIT = cfg.get("rate_limit_ms", 0)


MYSQL_CONFIG = cfg.get("mysql", {
    "host": "localhost",
    "user": "tDB",
    "password": "1234",
    "database": "csv_import"
})
