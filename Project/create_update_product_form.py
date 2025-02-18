import pyodbc
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QListWidget, QComboBox, QMessageBox, QRadioButton,
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
    """Return global connection and cursor."""
    return cnxn, cursor

class create_update_product_form(QWidget): 

    @staticmethod
    def create_update_product_form():
        """Create the form for updating product information."""
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)

        # Title
        title = QLabel("Update Product")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        form_layout.addWidget(title)

        # Dropdown for product names
        product_name_dropdown = create_update_product_form.create_dropdown_from_db("SELECT Product_Name FROM tbl_Product")
        product_name_dropdown.setFont(QFont("Arial", 14))
        form_layout.addWidget(product_name_dropdown)

        # Input fields for price and shelf life
        price_label = QLabel("Price:")
        price_label.setFont(QFont("Arial", 14))
        price_input = QLineEdit()
        price_input.setFont(QFont("Arial", 14))
        form_layout.addWidget(price_label)
        form_layout.addWidget(price_input)

        shelf_life_label = QLabel("Shelf Life (Months):")
        shelf_life_label.setFont(QFont("Arial", 14))
        shelf_life_input = QLineEdit()
        shelf_life_input.setFont(QFont("Arial", 14))
        form_layout.addWidget(shelf_life_label)
        form_layout.addWidget(shelf_life_input)

        # Button to fetch product details
        fetch_button = QPushButton("Fetch Details")
        fetch_button.setFont(QFont("Arial", 14, QFont.Bold))
        fetch_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        fetch_button.clicked.connect(lambda: create_update_product_form.fetch_product_details(product_name_dropdown, price_input, shelf_life_input))
        form_layout.addWidget(fetch_button)

        # Submit button to update product
        update_button = QPushButton("Update Product")
        update_button.setFont(QFont("Arial", 14, QFont.Bold))
        update_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        update_button.clicked.connect(lambda: create_update_product_form.update_product(product_name_dropdown, price_input, shelf_life_input))
        form_layout.addWidget(update_button)

        return form_frame

    @staticmethod
    def create_dropdown_from_db(query):
        """Create a dropdown populated from the database, filtering out deleted products."""
        combo_box = QComboBox()
        try:
            # Modify the query to include filtering for non-deleted products if needed
            if "tbl_Product" in query:  # Check if the query is for the product table
                query += " WHERE IsDeleted = 0"
            
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                combo_box.addItem(row[0])  # Assuming the first column holds the relevant items

        except pyodbc.Error as e:
            create_update_product_form.show_alert(f"An error occurred while loading dropdown: {str(e)}")
        
        return combo_box

    @staticmethod
    def fetch_product_details(product_name_dropdown, price_input, shelf_life_input):
        """Fetch product details based on the selected product."""
        product_name = product_name_dropdown.currentText()
        if not product_name:
            create_update_product_form.show_alert("Please select a product.")
            return
        
        # Query to get the current details for the selected product
        query = "SELECT Price, Shelf_Life FROM tbl_Product WHERE Product_Name = ?"
        
        try:
            cursor.execute(query, (product_name,))
            row = cursor.fetchone()
            if row:
                # Populate the fields with the current product details
                price_input.setText(str(row[0]))
                shelf_life_input.setText(str(row[1]))
            else:
                create_update_product_form.show_alert("Product not found.")
        except pyodbc.Error as e:
            create_update_product_form.show_alert(f"An error occurred: {str(e)}")

    @staticmethod
    def update_product(product_name_dropdown, price_input, shelf_life_input):
        """Update the selected product's price and/or shelf life using a stored procedure.
        The price history logging is handled by a trigger."""
        product_name = product_name_dropdown.currentText()
        price = price_input.text()
        shelf_life = shelf_life_input.text()

        # Ensure at least one field is filled
        if not price and not shelf_life:
            create_update_product_form.show_alert("Please fill in at least one field.")
            return

        try:
            # Prepare parameters for the stored procedure
            parameters = [
                product_name,
                float(price) if price else None,   # Convert to float for SQL compatibility
                float(shelf_life) if shelf_life else None  # Convert to int for SQL compatibility
            ]

            # Execute the stored procedure to update the product details
            cursor.execute("{CALL UpdateProductDetails (?, ?, ?)}", parameters)

            # Commit the transaction
            cnxn.commit()

            # Display success message
            create_update_product_form.show_alert("Product updated successfully! ")
        except pyodbc.Error as e:
            cnxn.rollback()  # Rollback in case of any error
            create_update_product_form.show_alert(f"An error occurred: {str(e)}")

    @staticmethod
    def show_alert(message):
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Information)
        alert.setText(message)
        alert.setWindowTitle("Alert")
        alert.exec_()
