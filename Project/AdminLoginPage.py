import pyodbc
import sys
from AdminDashboard import AdminDashboard 
import AlertBox

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QFrame, QListWidget, QComboBox, QMessageBox, QRadioButton,
    QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer

# Database connection
conn_str = (
    r'DRIVER={ODBC Driver 17 For SQL Server};'
    r'SERVER=(local)\SQLEXPRESS;'
    r'DATABASE=db_gardening_shop;'
    r'Trusted_Connection=yes;'
)
cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()
def get_db_connection():
    # Returning global connection and cursor
    return cnxn, cursor

class AdminLoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login - Gardening Shop")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        # Set the background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#e8f5e9"))  # Light green background
        self.setPalette(palette)

        # Create a vertical layout for the form
        form_layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel("Gardening Shop Admin Login")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #1b5e20;")  # Dark green text
        form_layout.addWidget(self.title_label)

        # Username label and input
        self.username_label = QLabel("Username:")
        self.username_label.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter admin username")
        self.username_input.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.username_input)

        # Password label and input
        self.password_label = QLabel("Password:")
        self.password_label.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter admin password")
        self.password_input.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.login_button.setStyleSheet(
            "background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;"
        )
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        self.setLayout(form_layout)

    def handle_login(self):
        # Hardcoded admin credentials
        admin_username = "admin"
        admin_password = "123"

        # Get user input
        username = self.username_input.text()
        password = self.password_input.text()

        # Check credentials
        if username == admin_username and password == admin_password:
            self.username_input.clear()  # Clear input fields
            self.password_input.clear()
            self.open_dashboard()
        else:
            self.show_alert("Invalid username or password!")

    def show_alert(self, message):
        alert = AlertBox(message, self)
        alert.show()

    def open_dashboard(self):
        self.dashboard = AdminDashboard()
        self.dashboard.show()
        self.close()