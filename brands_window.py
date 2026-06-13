from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit,
    QHBoxLayout, QMessageBox,
    QHeaderView
)

from db import get_connection


class BrandsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Бренды")
        self.resize(900, 600)

        layout = QVBoxLayout()

        title = QLabel("Список брендов")
        layout.addWidget(title)

        # ===== INPUT =====
        form = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название бренда")

        self.add_btn = QPushButton("Добавить")
        self.del_btn = QPushButton("Удалить")

        self.add_btn.clicked.connect(self.add_brand)
        self.del_btn.clicked.connect(self.delete_brand)

        form.addWidget(self.name_input)
        form.addWidget(self.add_btn)
        form.addWidget(self.del_btn)

        layout.addLayout(form)

        # ===== TABLE =====
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.setLayout(layout)

        self.load_data()

        # ===== STYLE (КАК У OWNER) =====
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

    def load_data(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name
            FROM automobile.brand
            ORDER BY id
        """)

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(["ID", "Название"])

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        cur.close()
        conn.close()

    # ===== ADD =====
    def add_brand(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название бренда")
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO automobile.brand (name)
            VALUES (%s)
        """, (name,))

        conn.commit()
        cur.close()
        conn.close()

        self.name_input.clear()
        self.load_data()

    # ===== DELETE =====
    def delete_brand(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выбери бренд")
            return

        brand_id = self.table.item(row, 0).text()

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                DELETE FROM automobile.brand
                WHERE id = %s
            """, (brand_id,))

            conn.commit()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

        cur.close()
        conn.close()

        self.load_data()