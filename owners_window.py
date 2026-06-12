from PyQt6.QtWidgets import(
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)
from PyQt6.QtWidgets import QHeaderView

from db import get_connection


class OwnersWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Владельцы")
        self.resize(900, 600)

        layout = QVBoxLayout()

        title = QLabel("Список владельцев")
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
            SELECT o.id, o.full_name, c.name
                FROM automobile.owner o
                LEFT JOIN automobile.country c
                    ON o.country_id = c.id
                ORDER BY o.id
        """)

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "ФИО",
            "Страна"
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

        for i, rows in enumerate(rows):
            for j, value in enumerate(rows):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        cur.close()
        conn.close()