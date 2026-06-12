from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem
import psycopg2
import traceback
from PyQt6.QtWidgets import QHeaderView


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="automobile_clean",
        user="postgres",
        password="eien1984freedom"
    )


class ReportsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Отчёты")
        self.resize(900, 600)

        layout = QVBoxLayout()

        self.btn_brand = QPushButton("По брендам")
        self.btn_power = QPushButton("Мощные авто")
        self.btn_country = QPushButton("По странам")
        self.btn_hall = QPushButton("По залам")
        self.btn_rare = QPushButton("Самые редкие")
        self.btn_old = QPushButton("Старейшие автомобили музея")
        for btn in [
            self.btn_brand,
            self.btn_power,
            self.btn_country,
            self.btn_hall,
            self.btn_rare,
            self.btn_old
        ]:
            btn.setMinimumHeight(45)

        self.table = QTableWidget()
        self.table.hide()
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setStyleSheet("""
        QTableWidget {
            background-color: white;
            gridline-color: #cccccc;
            font-size: 13px;
        }

        QHeaderView::section {
            background-color: #d9ccff;
            color: black;
            padding: 6px;
            border: 1px solid #bbbbbb;
            font-weight: bold;
        }
        """)

        layout.addWidget(self.btn_brand)
        layout.addWidget(self.btn_power)
        layout.addWidget(self.btn_country)
        layout.addWidget(self.btn_hall)
        layout.addWidget(self.btn_rare)
        layout.addWidget(self.btn_old)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStyleSheet("""
            QPushButton {
                background-color: #6B5FD6;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #5848C2;
            }
        """)

        self.btn_brand.clicked.connect(self.report_by_brand)
        self.btn_power.clicked.connect(self.report_power)
        self.btn_country.clicked.connect(self.report_by_country)
        self.btn_hall.clicked.connect(self.report_by_hall)
        self.btn_rare.clicked.connect(self.report_by_rare)
        self.btn_old.clicked.connect(self.report_by_old)

    # 1. По брендам
    def report_by_brand(self):
        self.table.show()
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT b.name, COUNT(a.id)
            FROM automobile.auto a
            JOIN automobile.brand b ON a.brand_id = b.id
            GROUP BY b.name
            ORDER BY COUNT(a.id) DESC;
        """)

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Бренд", "Количество"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: #8A6EFF;
                color: white;
                padding: 5px;
                font-weight: bold;
            }

            QTableWidget {
                gridline-color: #cccccc;
                background-color: white;
                color: #333333;
                alternate-background-color: #F4F1FF;
            }
        """)

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        cur.close()
        conn.close()

    # 2. Мощные авто
    def report_power(self):
        self.table.show()
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT model, engine_power, year_prod
            FROM automobile.auto 
            WHERE engine_power > 300
            ORDER BY engine_power DESC;
        """)

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Модель", "Мощность", "Год"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: #8A6EFF;
                color: white;
                padding: 5px;
                font-weight: bold;
            }

            QTableWidget {
                gridline-color: #cccccc;
                background-color: white;
                color: #333333;
                alternate-background-color: #F4F1FF;
            }
        """)

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        cur.close()
        conn.close()

    # 3. По странам
    def report_by_country(self):
        self.table.show()
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT c.name, COUNT(a.id)
                FROM automobile.auto a
                JOIN automobile.country c ON a.country_id = c.id
                GROUP BY c.name
                ORDER BY COUNT(a.id) DESC;
            """)

            rows = cur.fetchall()

            print(rows)

            self.table.setRowCount(len(rows))
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(["Страна", "Количество"])
            self.table.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.Stretch
            )
            self.table.setAlternatingRowColors(True)
            self.table.setStyleSheet("""
                QHeaderView::section {
                    background-color: #8A6EFF;
                    color: white;
                    padding: 5px;
                    font-weight: bold;
                }

                QTableWidget {
                    gridline-color: #cccccc;
                    background-color: white;
                    color: #333333;
                    alternate-background-color: #F4F1FF;
                }
            """)

            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))

            cur.close()
            conn.close()

        except Exception:
            traceback.print_exc()

    def report_by_hall(self):
        self.table.show()
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT h.room_number, COUNT(a.id)
            FROM automobile.hall h
            LEFT JOIN automobile.auto a ON a.hall_id = h.id
            GROUP BY h.room_number
            ORDER BY h.room_number;
        """)

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Зал", "Количество авто"])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: #8A6EFF;
                color: white;
                padding: 5px;
                font-weight: bold;
            }

            QTableWidget {
                gridline-color: #cccccc;
                background-color: white;
                color: #333333;
                alternate-background-color: #F4F1FF;
            }
        """)

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        cur.close()
        conn.close()

    def report_by_rare(self):
        self.table.show()
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT model, world_left_count
            FROM automobile.auto
            ORDER BY world_left_count ASC
            LIMIT 10;
        """)

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Модель", "Осталось в мире"])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: #8A6EFF;
                color: white;
                padding: 5px;
                font-weight: bold;
            }

            QTableWidget {
                gridline-color: #cccccc;
                background-color: white;
                color: #333333;
                alternate-background-color: #F4F1FF;
            }
        """)

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        cur.close()
        conn.close()

    def report_by_old(self):
        self.table.show()
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT model, year_prod
            FROM automobile.auto
            ORDER BY year_prod
            LIMIT 10;
        """)

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Модель", "Год выпуска"])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: #8A6EFF;
                color: white;
                padding: 5px;
                font-weight: bold;
            }

            QTableWidget {
                gridline-color: #cccccc;
                background-color: white;
                color: #333333;
                alternate-background-color: #F4F1FF;
            }
        """)


        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        cur.close()
        conn.close()