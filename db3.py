import sqlite3
import random
import string
from contextlib import closing

class ProductDB:
    def __init__(self, db_name='MyProduct.db'):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with closing(self.get_connection()) as conn, conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    productID INTEGER PRIMARY KEY,
                    productName TEXT NOT NULL,
                    productPrice INTEGER NOT NULL
                );
            ''')

    def insert_product(self, product_id, product_name, product_price):
        with closing(self.get_connection()) as conn, conn:
            conn.execute('''
                INSERT INTO Products (productID, productName, productPrice)
                VALUES (?, ?, ?)
            ''', (product_id, product_name, product_price))

    def update_product(self, product_id, product_name=None, product_price=None):
        if product_name is None and product_price is None:
            return
        fields = []
        values = []
        if product_name is not None:
            fields.append("productName = ?")
            values.append(product_name)
        if product_price is not None:
            fields.append("productPrice = ?")
            values.append(product_price)
        values.append(product_id)
        with closing(self.get_connection()) as conn, conn:
            conn.execute(f'''
                UPDATE Products SET {', '.join(fields)}
                WHERE productID = ?
            ''', values)

    def delete_product(self, product_id):
        with closing(self.get_connection()) as conn, conn:
            conn.execute('''
                DELETE FROM Products WHERE productID = ?
            ''', (product_id,))

    def select_product(self, product_id):
        with closing(self.get_connection()) as conn:
            cur = conn.execute('''
                SELECT productID, productName, productPrice
                FROM Products WHERE productID = ?
            ''', (product_id,))
            return cur.fetchone()

    def select_all(self, limit=100, offset=0):
        with closing(self.get_connection()) as conn:
            cur = conn.execute('''
                SELECT productID, productName, productPrice
                FROM Products ORDER BY productID
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            return cur.fetchall()

    def bulk_insert(self, items):
        with closing(self.get_connection()) as conn, conn:
            conn.executemany('''
                INSERT OR IGNORE INTO Products (productID, productName, productPrice)
                VALUES (?, ?, ?)
            ''', items)

def random_product_name(idx):
    # 예: ProductA1, ProductR2 ...
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    return f'Product{letters}{idx}'

def populate_sample_data(db, n=100000, batch=5000):
    print(f"샘플 데이터 {n}건 생성 중...")
    for start in range(1, n+1, batch):
        batch_items = []
        end = min(start + batch - 1, n)
        for i in range(start, end + 1):
            batch_items.append((i, random_product_name(i), random.randint(1000, 500000)))
        db.bulk_insert(batch_items)
        if start % (batch*4) == 1:
            print(f"  {end}개 처리 완료")
    print("샘플 데이터 준비 완료.")

if __name__ == "__main__":
    db = ProductDB('MyProduct.db')

    # 1) 샘플 100,000개 생성
    populate_sample_data(db, n=100000)

    # 2) CRUD 테스트
    db.insert_product(100001, "TestProduct", 99999)
    print("insert:", db.select_product(100001))

    db.update_product(100001, productName="TestProductUpdated", productPrice=123456)
    print("update:", db.select_product(100001))

    db.delete_product(100001)
    print("delete:", db.select_product(100001))

    # 3) 일부 조회
    print("first 5:", db.select_all(limit=5))