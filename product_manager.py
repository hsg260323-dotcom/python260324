import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)
from PyQt6.QtCore import Qt

DB_PATH = "products.db"

class ProductManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("자전거용품 관리")
        self.resize(600, 450)

        self.conn = sqlite3.connect(DB_PATH)
        self.create_table()

        self.init_ui()
        self.load_products()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS MyProduct (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL
                )
                """
            )

    def init_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #f0f4fb; color: #2b3e5c; font-family: 'Malgun Gothic', 'Arial', sans-serif; }
            QLabel { font-weight: bold; font-size: 13px; }
            QLineEdit { background-color: #ffffff; border: 1px solid #c4d3e7; border-radius: 6px; padding: 5px; min-height: 26px; }
            QPushButton { background-color: #476bb3; color: #ffffff; border-radius: 8px; padding: 8px 16px; font-size: 13px; }
            QPushButton:hover { background-color: #5d80d1; }
            QPushButton:pressed { background-color: #3b57a0; }
            QTableWidget { background-color: #ffffff; border: 1px solid #cdd9ee; gridline-color: #dce4f2; }
            QHeaderView::section { background-color: #3f6fb5; color: #ffffff; border: none; padding: 6px; font-size: 13px; }
            QTableWidget::item:selected { background-color: #9fc6ff; color: #1a2f56; }
        """
        )

        main_layout = QVBoxLayout()

        # Input row
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("ID:"))
        self.id_edit = QLineEdit()
        self.id_edit.setPlaceholderText("Auto (수정/삭제 시 사용)")
        input_layout.addWidget(self.id_edit)

        input_layout.addWidget(QLabel("이름:"))
        self.name_edit = QLineEdit()
        input_layout.addWidget(self.name_edit)

        input_layout.addWidget(QLabel("가격:"))
        self.price_edit = QLineEdit()
        input_layout.addWidget(self.price_edit)

        main_layout.addLayout(input_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.insert_btn = QPushButton("입력")
        self.insert_btn.clicked.connect(self.insert_product)
        button_layout.addWidget(self.insert_btn)

        self.update_btn = QPushButton("수정")
        self.update_btn.clicked.connect(self.update_product)
        button_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("삭제")
        self.delete_btn.clicked.connect(self.delete_product)
        button_layout.addWidget(self.delete_btn)

        self.search_btn = QPushButton("검색")
        self.search_btn.clicked.connect(self.search_product)
        button_layout.addWidget(self.search_btn)

        self.refresh_btn = QPushButton("전체")
        self.refresh_btn.clicked.connect(self.load_products)
        button_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(button_layout)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "이름", "가격"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.cellClicked.connect(self.on_table_click)

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def execute_query(self, query, params=()):
        try:
            with self.conn:
                cursor = self.conn.execute(query, params)
            return cursor
        except sqlite3.Error as e:
            QMessageBox.critical(self, "DB 오류", str(e))
            return None

    def insert_product(self):
        name = self.name_edit.text().strip()
        price_text = self.price_edit.text().strip()
        if not name or not price_text:
            QMessageBox.warning(self, "입력 오류", "이름과 가격을 모두 입력하세요.")
            return

        if not price_text.isdigit():
            QMessageBox.warning(self, "입력 오류", "가격은 숫자만 입력하세요.")
            return

        self.execute_query(
            "INSERT INTO MyProduct (name, price) VALUES (?, ?)",
            (name, int(price_text)),
        )
        self.load_products()
        self.clear_inputs()

    def update_product(self):
        id_text = self.id_edit.text().strip()
        name = self.name_edit.text().strip()
        price_text = self.price_edit.text().strip()

        if not id_text.isdigit():
            QMessageBox.warning(self, "수정 오류", "수정할 항목의 ID를 입력하세요.")
            return

        if not name or not price_text:
            QMessageBox.warning(self, "수정 오류", "이름과 가격을 모두 입력하세요.")
            return

        if not price_text.isdigit():
            QMessageBox.warning(self, "수정 오류", "가격은 숫자만 입력하세요.")
            return

        self.execute_query(
            "UPDATE MyProduct SET name=?, price=? WHERE id=?",
            (name, int(price_text), int(id_text)),
        )
        self.load_products()
        self.clear_inputs()

    def delete_product(self):
        id_text = self.id_edit.text().strip()
        if not id_text.isdigit():
            QMessageBox.warning(self, "삭제 오류", "삭제할 항목의 ID를 입력하세요.")
            return

        ret = QMessageBox.question(
            self,
            "삭제 확인",
            f"ID {id_text} 항목을 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if ret != QMessageBox.StandardButton.Yes:
            return

        self.execute_query("DELETE FROM MyProduct WHERE id=?", (int(id_text),))
        self.load_products()
        self.clear_inputs()

    def search_product(self):
        keyword = self.name_edit.text().strip()
        if keyword == "":
            QMessageBox.warning(self, "검색 오류", "검색할 이름을 입력하세요.")
            return

        rows = self.execute_query(
            "SELECT id, name, price FROM MyProduct WHERE name LIKE ? ORDER BY id",
            (f"%{keyword}%",),
        )
        if rows is None:
            return

        self.populate_table(rows.fetchall())

    def load_products(self):
        rows = self.execute_query(
            "SELECT id, name, price FROM MyProduct ORDER BY id"
        )
        if rows is None:
            return

        self.populate_table(rows.fetchall())

    def populate_table(self, data):
        self.table.setRowCount(0)
        for row in data:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(r, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(r, 2, QTableWidgetItem(str(row[2])))

    def on_table_click(self, row, column):
        item_id = self.table.item(row, 0).text()
        item_name = self.table.item(row, 1).text()
        item_price = self.table.item(row, 2).text()

        self.id_edit.setText(item_id)
        self.name_edit.setText(item_name)
        self.price_edit.setText(item_price)

    def clear_inputs(self):
        self.id_edit.clear()
        self.name_edit.clear()
        self.price_edit.clear()

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ProductManager()
    w.show()
    sys.exit(app.exec())
