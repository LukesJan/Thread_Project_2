import mysql.connector
import threading

class MySQLConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.connection = mysql.connector.connect(
                    host="localhost",
                    user="tDB",
                    password="1234",
                    database="csv_import"
                )
            return cls._instance

    def get_connection(self):
        return self.connection
