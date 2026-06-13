from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton,
    QHBoxLayout, QInputDialog,
    QMessageBox
)

from db import get_connection


class CarsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Автомобили")
        self.resize(900, 600)

        layout = QVBoxLayout()

        title = QLabel("Список автомобилей")
        layout.addWidget(title)

        # кнопки
        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("Добавить")
        self.btn_delete = QPushButton("Удалить")

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)

        layout.addLayout(btn_layout)

        self.btn_add.clicked.connect(self.add_car)
        self.btn_delete.clicked.connect(self.delete_car)

        self.table = QTableWidget()
        layout.addWidget(self.table)

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

        self.setLayout(layout)

        self.load_data()

        # стиль оставил как у тебя (НЕ ТРОГАЮ ВИЗУАЛ)

    def load_data(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                a.id,
                b.name,
                a.model,
                a.year_prod,
                a.engine_power,
                h.room_number,
                a.engine_volume,
                bt.name,
                a.original_parts_percent,
                a.world_left_count,
                o.full_name
            FROM automobile.auto a
            JOIN automobile.brand b
                ON a.brand_id = b.id
            LEFT JOIN automobile.hall h
                ON a.hall_id = h.id
            LEFT JOIN automobile.body_type bt
                ON a.body_type_id = bt.id
            LEFT JOIN automobile.owner o
                ON a.owner_id = o.id
            ORDER BY a.id
        """)

        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(11)

        self.table.setHorizontalHeaderLabels([
            "ID", "Марка", "Модель", "Год", "Мощность",
            "Зал", "Объём", "Кузов", "Оригинал %",
            "В мире", "Владелец"
        ])

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        cur.close()
        conn.close()

    # -------------------------
    # УДАЛЕНИЕ
    # -------------------------
    def delete_car(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выбери машину")
            return

        car_id = self.table.item(row, 0).text()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM automobile.auto WHERE id = %s", (car_id,))

        conn.commit()
        cur.close()
        conn.close()

        self.load_data()

    # -------------------------
    # ДОБАВЛЕНИЕ (ИСПРАВЛЕНО)
    # -------------------------
    def add_car(self):
        try:
            brand_id = QInputDialog.getInt(self, "Brand ID", "ID бренда:")[0]
            model = QInputDialog.getText(self, "Модель", "Модель:")[0]
            year = QInputDialog.getInt(self, "Год", "Год:")[0]
            power = QInputDialog.getInt(self, "Мощность", "Мощность:")[0]
            volume = QInputDialog.getDouble(self, "Объём", "Объём двигателя:")[0]
            body_type_id = QInputDialog.getInt(self, "Body Type ID", "ID кузова:")[0]
            original = QInputDialog.getDouble(self, "Оригинал %", "Процент:")[0]
            world = QInputDialog.getInt(self, "В мире", "Количество:")[0]
            owner_id = QInputDialog.getInt(self, "Owner ID", "ID владельца:")[0]
            hall_id = QInputDialog.getInt(self, "Hall ID", "ID зала:")[0]

            conn = get_connection()
            cur = conn.cursor()

            # проверки (как у тебя уже сделано, просто аккуратно расширено)

            cur.execute("SELECT id FROM automobile.brand WHERE id=%s", (brand_id,))
            if not cur.fetchone():
                raise Exception("Сначала добавь бренд в раздел 'Бренды'")

            cur.execute("SELECT id FROM automobile.owner WHERE id=%s", (owner_id,))
            if not cur.fetchone():
                raise Exception("Владелец не найден")

            cur.execute("SELECT id FROM automobile.hall WHERE id=%s", (hall_id,))
            if not cur.fetchone():
                raise Exception("Зал не найден")

            cur.execute("SELECT id FROM automobile.body_type WHERE id=%s", (body_type_id,))
            if not cur.fetchone():
                raise Exception("Тип кузова не найден")

            cur.execute("""
                INSERT INTO automobile.auto (
                    brand_id, model, year_prod,
                    engine_power, engine_volume,
                    body_type_id,
                    original_parts_percent,
                    world_left_count,
                    hall_id,
                    owner_id
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                brand_id, model, year,
                power, volume,
                body_type_id,
                original,
                world,
                hall_id,
                owner_id
            ))

            conn.commit()
            cur.close()
            conn.close()

            self.load_data()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
