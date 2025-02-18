import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pyodbc

def get_db_connection():
    conn_str = (
        r'DRIVER={ODBC Driver 17 For SQL Server};'
        r'SERVER=(local)\SQLEXPRESS;'
        r'DATABASE=db_gardening_shop;'
        r'Trusted_Connection=yes;'
    )
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    return cnxn, cursor

class ShipmentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.cnxn, self.cursor = get_db_connection()
        self.shipments = []  # List to store added shipments temporarily
        self.purchase_id = None  # Variable to store Purchase_ID for the current session
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI components"""
        self.setWindowTitle("Shipment Entry Form")
        main_layout = QVBoxLayout()

        # Title
        title_label = QLabel("Shipment Entry Form")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #1b5e20;")
        main_layout.addWidget(title_label)

        # Shipment Name dropdown
        self.name_label = QLabel("Name:")
        self.name_label.setFont(QFont("Arial", 15))
        self.name_dropdown = QComboBox()
        self.name_dropdown.setMinimumWidth(300)
        self.populate_name_dropdown()
        main_layout.addWidget(self.name_label)
        main_layout.addWidget(self.name_dropdown)

        # Price input field
        self.price_label = QLabel("Price:")
        self.price_label.setFont(QFont("Arial", 15))
        self.price_input = QLineEdit()
        self.price_input.setMinimumWidth(250)
        main_layout.addWidget(self.price_label)
        main_layout.addWidget(self.price_input)

        # Quantity input field
        self.quantity_label = QLabel("Quantity:")
        self.quantity_label.setFont(QFont("Arial", 15))
        self.quantity_input = QLineEdit()
        self.quantity_input.setMinimumWidth(250)
        main_layout.addWidget(self.quantity_label)
        main_layout.addWidget(self.quantity_input)

        # Done Button
        self.done_button = QPushButton("Done")
        self.done_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.done_button.setStyleSheet(
            "background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;"
        )
        self.done_button.clicked.connect(self.add_shipment)
        main_layout.addWidget(self.done_button)

        # Add Another Shipment Button
        self.add_another_button = QPushButton("Add Another Shipment")
        self.add_another_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.add_another_button.setStyleSheet(
            "background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;"
        )
        self.add_another_button.clicked.connect(self.add_to_shipment_list)
        main_layout.addWidget(self.add_another_button)

        self.setLayout(main_layout)

    def populate_name_dropdown(self):
        """Populate the dropdown with product names from the database."""
        query = "SELECT Product_Name FROM tbl_Product WHERE IsDeleted = 0"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            product_names = [row[0] for row in rows]
            self.name_dropdown.addItems(product_names)
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load product names: {str(e)}")

    def add_shipment(self):
        """Handle the 'Done' button click - Add all shipments using a single procedure."""
        self.add_to_shipment_list()

        if not self.shipments:
            QMessageBox.warning(self, "No Shipments", "No products were added to the shipment.")
            return

        try:
            for shipment in self.shipments:
                product_name, price, quantity = shipment

                # Call the stored procedure to handle everything
                self.cursor.execute("{CALL sp_AddShipment (?, ?, ?)}", product_name, quantity, price)
                self.cnxn.commit()

            QMessageBox.information(self, "Success", "All Shipments Added and Products Updated Successfully!")
            self.shipments.clear()
            self.clear_inputs()

        except pyodbc.Error as e:
            self.cnxn.rollback()
            QMessageBox.critical(self, "Database Error", f"Failed to add shipment: {str(e)}")

    def add_to_shipment_list(self):
        """Add a shipment to the temporary shipment list."""
        name = self.name_dropdown.currentText()
        price = self.price_input.text()
        quantity = self.quantity_input.text()

        if not name or not price or not quantity:
            QMessageBox.warning(self, "Input Error", "All fields must be filled.")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, "Input Error", 
                              "Price must be a number and quantity an integer.")
            return

        self.shipments.append((name, price, quantity))
        self.clear_inputs()
        QMessageBox.information(self, "Success", "Product added to shipment list!")

    def clear_inputs(self):
        """Clear all input fields for adding another shipment."""
        self.price_input.clear()
        self.quantity_input.clear()
        self.name_dropdown.setCurrentIndex(0)