import mysql.connector
from config import MYSQL_CONFIG
from error_logger import ErrorLogger

error_logger = ErrorLogger()

class ProductDAO:
    """
    Data Access Object for the 'products' table

    Methods:
    __init__():
        - Establishes a connection to MySQL using MYSQL_CONFIG.
        - Logs an error if the connection fails and sets self.conn to None

    insert_many(items):
        - Inserts multiple product records into the 'products' table in a single batch.
        - items: list of tuples (name, category, price, quantity)
        - Commits the transaction and closes the cursor
        - Logs any database errors that occur.
    """
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**MYSQL_CONFIG)
        except Exception as e:
            from error_logger import ErrorLogger
            logger = ErrorLogger()
            logger.log(f"MySQL connection failed: {e}")
            self.conn = None

    def insert_many(self, items):
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            cursor.executemany(
                "INSERT INTO products (name, category, price, quantity) VALUES (%s, %s, %s, %s)",
                items
            )
            self.conn.commit()
            cursor.close()
        except Exception as e:
            from error_logger import ErrorLogger
            logger = ErrorLogger()
            logger.log(f"DB insert failed: {e}")

