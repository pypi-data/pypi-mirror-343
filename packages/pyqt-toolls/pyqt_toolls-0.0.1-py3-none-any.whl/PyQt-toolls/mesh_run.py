import pymysql, sys
from PyQt5.QtWidgets import *

class LoginWindow(QDialog):
    def init(self):
        super().init()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout(self)
        self.email_input = QLineEdit(placeholderText="Email")
        self.password_input = QLineEdit(placeholderText="Пароль", echoMode=QLineEdit.Password)
        layout.addWidget(QLabel("Вход в систему"))
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(QPushButton("Войти", clicked=self.attempt_login))
        self.db = pymysql.connect(host="localhost", user="root", password="", db="carpet_shop", charset="utf8mb4")
        self.cursor = self.db.cursor()
        self.user_id = self.user_role = None

    def attempt_login(self):
        email, password = self.email_input.text(), self.password_input.text()
        if not email or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        try:
            self.cursor.execute("SELECT id, role FROM users WHERE email=%s AND password_hash=%s", (email, password))
            user = self.cursor.fetchone()
            if user: self.user_id, self.user_role = user; self.accept()
            else: QMessageBox.warning(self, "Ошибка", "Неверный email или пароль")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка БД: {e}")

class CarpetOrderApp(QMainWindow):
    def init(self, user_id, user_role):
        super().init()
        self.user_id, self.user_role = user_id, user_role
        self.setWindowTitle(f"Шелковпарк - Заказ ковров (Пользователь: {user_role})")
        self.setGeometry(100, 100, 600, 400)
        self.db = pymysql.connect(host="localhost", user="root", password="", db="carpet_shop", charset="utf8mb4")
        self.cursor = self.db.cursor()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        w = self.widgets = {
            'carpets': QComboBox(), 'material': QComboBox(), 'edge': QComboBox(),
            'width': QLineEdit(placeholderText="Ширина (м)"),
            'height': QLineEdit(placeholderText="Длина (м)"),
            'quantity': QLineEdit(placeholderText="Количество"),
            'order_btn': QPushButton("Оформить заказ", clicked=self.place_order)
        }
        layout = QVBoxLayout()
        for label, widget in [("Ковер", w['carpets']), ("Материал", w['material']), ("Окантовка", w['edge']),
                              ("", w['width']), ("", w['height']), ("", w['quantity']), ("", w['order_btn'])]:
            if label: layout.addWidget(QLabel(label))
            layout.addWidget(widget)
        central = QWidget(); central.setLayout(layout); self.setCentralWidget(central)

    def load_data(self):
        for combo, query in [(self.widgets['material'], "SELECT id, model FROM materials"),
                             (self.widgets['edge'], "SELECT id, name FROM edge_types")]:
            combo.clear(); self.cursor.execute(query); rows = self.cursor.fetchall()
            combo.addItems([r[1] for r in rows])
            for i, r in enumerate(rows): combo.setItemData(i, r[0])
        self.load_carpets()

    def load_carpets(self):
        combo = self.widgets['carpets']; combo.clear()
        self.cursor.execute("SELECT id, name FROM carpets"); rows = self.cursor.fetchall()
        combo.addItems([r[1] for r in rows])
        for i, r in enumerate(rows): combo.setItemData(i, r[0])

Артур Ахи 🐺, [25.04.2025 22:20]
def place_order(self):
        try:
            w = self.widgets
            width, height, qty = float(w['width'].text()), float(w['height'].text()), float(w['quantity'].text())
            cid, eid = w['carpets'].currentData(), w['edge'].currentData()
            self.cursor.execute("SELECT price_per_m2 FROM carpets WHERE id=%s", (cid,))
            price = self.cursor.fetchone()[0] * width * height * qty
            if price > 10000: price *= 1 - (0.05 if price <= 50000 else 0.10 if price <= 100000 else 0.15)
            self.cursor.execute("INSERT INTO orders (user_id) VALUES (%s)", (self.user_id,))
            oid = self.cursor.lastrowid
            self.cursor.execute("""INSERT INTO order_items 
                (order_id, carpet_id, edge_type_id, width, height, quantity, price) 
                VALUES (%s,%s,%s,%s,%s,%s,%s)""", (oid, cid, eid, width, height, qty, price))
            self.db.commit()
            QMessageBox.information(self, "Успех", f"Заказ оформлен! Цена: {price:.2f} руб.")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения")
        except Exception as e:
            self.db.rollback(); QMessageBox.critical(self, "Ошибка", f"Ошибка заказа: {e}")

if name == "main":
    app = QApplication(sys.argv)
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        window = CarpetOrderApp(login.user_id, login.user_role)
        window.show()
        sys.exit(app.exec_())
    sys.exit()