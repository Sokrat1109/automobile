from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt6.QtWidgets import QHeaderView

from db import get_connection


class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Поиск автомобилей")
        self.resize(900, 600)

        layout = QVBoxLayout()

        self.label = QLabel("Поиск по модели")
        layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите часть модели (например: Supra)")
        layout.addWidget(self.input)

        self.btn = QPushButton("Найти")
        self.btn.clicked.connect(self.search)
        layout.addWidget(self.btn)

        self.table = QTableWidget()
        self.table.hide()
        layout.addWidget(self.table)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.setLayout(layout)

    def search(self):
        self.table.show()
        text = self.input.text()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT a.id, b.name, a.model, a.year_prod, a.engine_power
                FROM automobile.auto a
                JOIN automobile.brand b ON a.brand_id = b.id
                WHERE a.model ILIKE %s
                ORDER BY a.id
        """, (f"%{text}%",))

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "ID", "Марка", "Модель", "Год", "Мощность"
        ])
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
