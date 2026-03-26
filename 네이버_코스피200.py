import sys
import requests
from bs4 import BeautifulSoup
import csv
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal
from openpyxl import Workbook

class CrawlingThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)

    def run(self):
        all_data = []
        total_pages = 20
        for page in range(1, total_pages + 1):
            url = f"https://finance.naver.com/sise/entryJongmok.naver?type=KPI200&page={page}"

            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                header = soup.find('h4', class_='top_tlt')
                if not header or '편입종목상위' not in header.text:
                    continue

                table = header.find_next('table', class_='type_1')
                if not table:
                    continue

                rows = table.find_all('tr')
                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) >= 7:
                        종목명 = cols[0].find('a').text.strip() if cols[0].find('a') else cols[0].text.strip()
                        현재가 = cols[1].text.strip()
                        전일비_span = cols[2].find('span', class_='tah')
                        전일비_direction = cols[2].find('em').find('span', class_='blind').text.strip() if cols[2].find('em') else ''
                        전일비 = f"{전일비_direction} {전일비_span.text.strip()}" if 전일비_span else cols[2].text.strip()
                        등락률_span = cols[3].find('span', class_='tah')
                        등락률 = 등락률_span.text.strip() if 등락률_span else cols[3].text.strip()
                        거래량 = cols[4].text.strip()
                        거래대금 = cols[5].text.strip()
                        시가총액 = cols[6].text.strip()
                        all_data.append({
                            '종목명': 종목명,
                            '현재가': 현재가,
                            '전일비': 전일비,
                            '등락률': 등락률,
                            '거래량': 거래량,
                            '거래대금': 거래대금,
                            '시가총액': 시가총액
                        })
            except Exception as e:
                print(f"페이지 {page} 오류: {e}")

            self.progress.emit(page)

        self.finished.emit(all_data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("네이버 코스피200 크롤러")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.start_button = QPushButton("크롤링 시작")
        self.start_button.clicked.connect(self.start_crawling)
        self.layout.addWidget(self.start_button)

        self.progress_label = QLabel("진행 상황: 준비 중")
        self.layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(20)
        self.layout.addWidget(self.progress_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['종목명', '현재가', '전일비', '등락률', '거래량', '거래대금', '시가총액'])
        self.layout.addWidget(self.table)

        self.save_button = QPushButton("엑셀 저장")
        self.save_button.clicked.connect(self.save_excel)
        self.save_button.setEnabled(False)
        self.layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.data = []

    def start_crawling(self):
        self.start_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_label.setText("진행 상황: 크롤링 중...")
        self.thread = CrawlingThread()
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def update_progress(self, page):
        self.progress_bar.setValue(page)
        self.progress_label.setText(f"진행 상황: 페이지 {page}/20 완료")

    def on_finished(self, data):
        self.data = data
        self.progress_label.setText("진행 상황: 완료")
        self.start_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.populate_table()

    def populate_table(self):
        self.table.setRowCount(len(self.data))
        for row, item in enumerate(self.data):
            self.table.setItem(row, 0, QTableWidgetItem(item['종목명']))
            self.table.setItem(row, 1, QTableWidgetItem(item['현재가']))
            self.table.setItem(row, 2, QTableWidgetItem(item['전일비']))
            self.table.setItem(row, 3, QTableWidgetItem(item['등락률']))
            self.table.setItem(row, 4, QTableWidgetItem(item['거래량']))
            self.table.setItem(row, 5, QTableWidgetItem(item['거래대금']))
            self.table.setItem(row, 6, QTableWidgetItem(item['시가총액']))

    def save_excel(self):
        wb = Workbook()
        ws = wb.active
        if self.data:
            headers = list(self.data[0].keys())
            ws.append(headers)
            for row in self.data:
                ws.append(list(row.values()))
        wb.save('kospi200.xlsx')
        self.progress_label.setText("저장 완료: kospi200.xlsx")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
