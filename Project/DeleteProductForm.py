import pyodbc
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QFrame, QListWidget, QComboBox, QMessageBox, QRadioButton,
    QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

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
    """Returns the global database connection and cursor."""
    return cnxn, cursor
#DELETE CLASS------------------------------
class DeleteProductForm(QWidget):
    def __init__(self):  
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI for the Delete Product form."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Header
        header = QLabel("DELETE PRODUCT")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Spacer to push the label and dropdown slightly down
        main_layout.addSpacing(50)

        # Layout for label and dropdown (left-center alignment)
        product_layout = QVBoxLayout()
        product_layout.setAlignment(Qt.AlignLeft)

        # Product Name Label
        label = QLabel("Product Name:")
        label.setFont(QFont("Arial", 16))
        label.setAlignment(Qt.AlignLeft)
        product_layout.addWidget(label)

        # Product Dropdown
        self.product_dropdown = QComboBox()
        self.product_dropdown.addItem("-- Select Product --")
        self.load_products()
        self.product_dropdown.setFixedWidth(300)
        product_layout.addWidget(self.product_dropdown, alignment=Qt.AlignLeft)

        # Add the product layout to the main layout
        main_layout.addLayout(product_layout)

        # Spacer to push the delete button down
        main_layout.addSpacing(50)

        # Delete Button
        delete_button = QPushButton("DELETE")
        delete_button.setStyleSheet(
            "background-color: #4caf50; color: white; padding: 15px; border-radius: 10px; font-weight: bold;"
        )
        delete_button.setFixedWidth(200)
        delete_button.clicked.connect(self.delete_product)
        main_layout.addWidget(delete_button, alignment=Qt.AlignCenter)

        # Set the main layout
        self.setLayout(main_layout)

    def load_products(self):
        """Load product names into the dropdown."""
        try:
            query = "SELECT Product_Name FROM tbl_Product WHERE IsDeleted = 0"
            cursor.execute(query)
            products = cursor.fetchall()
            for product in products:
                self.product_dropdown.addItem(product[0])
        except pyodbc.Error as e:
            QMessageBox.warning(self, "Error", f"Error loading products: {str(e)}")

    def delete_product(self):
        """Delete the selected product using the stored procedure."""
        product_name = self.product_dropdown.currentText()

        if product_name == "-- Select Product --":
            QMessageBox.warning(self, "Error", "Please select a product to delete.")
            return

        # Confirmation dialog
        confirmation = QMessageBox(self)
        confirmation.setIcon(QMessageBox.Warning)
        confirmation.setWindowTitle("Confirm Deletion")
        confirmation.setText(f"Are you sure you want to delete the product '{product_name}'?")
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)

        # If the user confirms, delete the product
        if confirmation.exec_() == QMessageBox.Yes:
            try:
                query = "EXEC sp_DeleteProductByName @ProductName = ?"
                cursor.execute(query, product_name)
                cnxn.commit()

                QMessageBox.information(self, "Success", f"Product '{product_name}' marked as deleted successfully.")

                # Refresh the dropdown
                self.product_dropdown.clear()
                self.product_dropdown.addItem("-- Select Product --")
                self.load_products()
            except pyodbc.Error as e:
                QMessageBox.critical(self, "Error", f"Error deleting product: {str(e)}")
