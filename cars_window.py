from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt6.QtWidgets import QHeaderView

from db import get_connection


class CarsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Автомобили")
        self.resize(900, 600)

        layout = QVBoxLayout()

        title = QLabel("Список автомобилей")
        layout.addWidget(title)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                a.id,
                b.name,
                a.model,
                a.year_prod,
                a.engine_power
            FROM automobile.auto a
            JOIN automobile.brand b
                ON a.brand_id = b.id
            ORDER BY a.id
        """)

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Марка",
            "Модель",
            "Год",
            "Мощность"
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
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        cur.close()
        conn.close()