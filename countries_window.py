from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QMessageBox
)

from db import get_connection


class CountriesWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Страны")
        self.resize(900, 600)

        layout = QVBoxLayout()

        title = QLabel("Список стран")
        layout.addWidget(title)

        # ===== ВВОД =====
        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название страны")

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_country)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_country)

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.add_btn)
        form_layout.addWidget(self.delete_btn)

        layout.addLayout(form_layout)

        # ===== ТАБЛИЦА =====
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
            SELECT id, name
            FROM automobile.country
            ORDER BY id
        """)

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels([
            "ID",
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

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        cur.close()
        conn.close()

    # ===== ДОБАВЛЕНИЕ =====
    def add_country(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название страны")
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO automobile.country (name)
            VALUES (%s)
        """, (name,))

        conn.commit()
        cur.close()
        conn.close()

        self.name_input.clear()
        self.load_data()

    # ===== УДАЛЕНИЕ =====
    def delete_country(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выбери страну")
            return

        country_id = self.table.item(row, 0).text()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM automobile.country
            WHERE id = %s
        """, (country_id,))

        conn.commit()
        cur.close()
        conn.close()

        self.load_data()