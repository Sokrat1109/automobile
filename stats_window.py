from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel
)
from PyQt6.QtWidgets import QHeaderView

import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="automobile_clean",
        user="postgres",
        password="eien1984freedom"
    )


class StatsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Статистика")
        self.resize(500,200)

        layout = QVBoxLayout()

        self.lbl_auto = QLabel()
        self.lbl_owner = QLabel()
        self.lbl_country = QLabel()
        self.lbl_brand = QLabel()

        layout.addWidget(self.lbl_auto)
        layout.addWidget(self.lbl_owner)
        layout.addWidget(self.lbl_country)
        layout.addWidget(self.lbl_brand)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.load_stats()

    def load_stats(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM automobile.auto")
        auto_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM automobile.owner")
        owner_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM automobile.country")
        country_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM automobile.brand")
        brand_count = cur.fetchone()[0]

        self.lbl_auto.setText(f"Автомобилей: {auto_count}")
        self.lbl_owner.setText(f"Владельцев: {owner_count}")
        self.lbl_country.setText(f"Стран: {country_count}")
        self.lbl_brand.setText(f"Брендов: {brand_count}")

        cur.close()
        conn.close()