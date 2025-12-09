from db import MySQLConnection

class ProductDAO:
    def __init__(self):
        self.conn = MySQLConnection().get_connection()

    def insert_record(self, name, category, price, quantity):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, category, price, quantity) VALUES (%s, %s, %s, %s)",
            (name, category, price, quantity)
        )
        self.conn.commit()
        cursor.close()

    def fetch_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, category, price, quantity FROM products")
        data = cursor.fetchall()
        cursor.close()
        return data
