import pyodbc
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QFrame, QListWidget, QComboBox, QMessageBox, QRadioButton,
    QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer

def __init__(self, message, parent=None):
    super().__init__(parent)
    self.setWindowTitle("Alert")
    self.setGeometry(600, 300, 300, 100)
    self.setStyleSheet("background-color: #ffeb3b; border-radius: 10px;")
    layout = QVBoxLayout()

    alert_message = QLabel(message)
    alert_message.setFont(QFont("Arial", 12))
    alert_message.setAlignment(Qt.AlignCenter)
    layout.addWidget(alert_message)

    self.setLayout(layout)

    # Automatically close after 3 seconds
    QTimer.singleShot(3000, self.close)

def show_alert(self, message):
    """This method will create a small alert box on the screen"""
    msg = QMessageBox(self)
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle("Alert")
    msg.setStyleSheet("background-color: #ffeb3b; color: black;")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.button(QMessageBox.Ok).setStyleSheet("background-color: #4caf50; color: white;")
    msg.exec_()
        