from cars_window import CarsWindow
from owners_window import OwnersWindow
from search_window import SearchWindow
from reports_window import ReportsWindow
from stats_window import StatsWindow
from countries_window import CountriesWindow
from brands_window import BrandsWindow
from body_type_window import BodyTypeWindow

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel,
    QMessageBox
)
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QFont

import sys
import psycopg2



def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="automobile_clean",
        user="postgres",
        password="eien1984freedom"
    )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cars_window = None
        self.owner_window = None
        self.search_window = None
        self.reports_window = None
        self.stats_window = None
        self.countries_window = None
        self.brands_window = None
        self.body_type_window = None

        self.setWindowTitle("Музей автомобилей")
        self.setGeometry(200, 200, 900, 600)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(80, 30, 80, 30)

        self.label = QLabel("Музей автомобилей")

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;

            border: 2px solid #8A6EFF;
            border-radius: 15px;
            
            background-color: transparent;
            padding: 15px;
            margin: 15px;
        """)

        layout.addWidget(self.label)

        self.btn_auto = QPushButton("Автомобили")
        layout.addWidget(self.btn_auto)
        self.btn_auto.clicked.connect(self.open_cars)

        self.btn_owner = QPushButton("Владельцы")
        layout.addWidget(self.btn_owner)
        self.btn_owner.clicked.connect(self.open_owners)

        self.btn_countries = QPushButton("Страны")
        layout.addWidget(self.btn_countries)
        self.btn_countries.clicked.connect(self.open_countries)

        self.btn_brands = QPushButton("Бренды")
        layout.addWidget(self.btn_brands)
        self.btn_brands.clicked.connect(self.open_brands)

        self.btn_body_type = QPushButton("Типы кузова")
        layout.addWidget(self.btn_body_type)
        self.btn_body_type.clicked.connect(self.open_body_type)

        self.btn_search = QPushButton("Поиск")
        layout.addWidget(self.btn_search)
        self.btn_search.clicked.connect(self.open_search)

        self.btn_reports = QPushButton("Отчеты")
        layout.addWidget(self.btn_reports)
        self.btn_reports.clicked.connect(self.open_reports)

        self.btn_stats = QPushButton("Статистика")
        layout.addWidget(self.btn_stats)
        self.btn_stats.clicked.connect(self.open_stats)

        self.btn_about = QPushButton("О программе")
        layout.addWidget(self.btn_about)
        self.btn_about.clicked.connect(self.show_about)

        self.btn_exit = QPushButton("Выход")
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit)

        for btn in [
            self.btn_auto,
            self.btn_owner,
            self.btn_brands,
            self.btn_countries,
            self.btn_body_type,
            self.btn_search,
            self.btn_reports,
            self.btn_stats,
            self.btn_about,
            self.btn_exit
        ]:
            btn.setMinimumHeight(45)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setStyleSheet("""
        QPushButton {
            background-color: qlineargradient(
                x1:0, y1:0,
                x2:1, y2:0,
                stop:0 #6ea8fe,
                stop:1 #d17cff
            );

            color: white;
            border: none;
            border-radius: 10px;

            padding: 10px;
            font-size: 14px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: qlineargradient(
                x1:0, y1:0,
                x2:1, y2:0,
                stop:0 #82b5ff,
                stop:1 #db95ff
            );
        }

        QPushButton:pressed {
            background-color: #8c6cff;
        }

        QLabel {
            font-size: 14px;
        }
        """)

    def open_cars(self):
        self.cars_window = CarsWindow()
        self.cars_window.show()

    def open_owners(self):
        self.owner_window = OwnersWindow()
        self.owner_window.show()

    def open_countries(self):
        self.countries_window = CountriesWindow()
        self.countries_window.show()

    def open_brands(self):
        self.brands_window = BrandsWindow()
        self.brands_window.show()

    def open_body_type(self):
        self.body_type_window = BodyTypeWindow()
        self.body_type_window.show()

    def open_search(self):
        self.search_window = SearchWindow()
        self.search_window.show()

    def open_reports(self):
        self.reports_window = ReportsWindow()
        self.reports_window.show()

    def open_stats(self):
        self.stats_window = StatsWindow()
        self.stats_window.show()

    def show_about(self):
        QMessageBox.information(
            self,
            "О программе",
            "Информационная система музея автомобилей\n\n"
            "Разработана для учёта автомобилей, владельцев и формирования отчётов."
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
