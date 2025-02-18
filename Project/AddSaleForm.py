import pyodbc
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QFrame, QListWidget, QComboBox, QMessageBox, QRadioButton,
    QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog
from datetime import datetime


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
class AddSaleForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Sale")
        self.sale_id = None  # This will store the Sale ID for this session
        self.products = []  # List to store products for the current sale
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Title
        title_label = QLabel("Add Sale")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #1b5e20;")
        main_layout.addWidget(title_label)

        # Form layout
        form_layout = QVBoxLayout()

        # Name dropdown
        self.name_label = QLabel("Name:")
        self.name_label.setFont(QFont("Arial", 14))
        self.name_dropdown = QComboBox()
        self.populate_name_dropdown()
        self.name_dropdown.setMinimumWidth(250)
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_dropdown)

        # Quantity input field
        self.quantity_label = QLabel("Quantity:")
        self.quantity_label.setFont(QFont("Arial", 14))
        self.quantity_input = QLineEdit()
        self.quantity_input.setMinimumWidth(250)
        form_layout.addWidget(self.quantity_label)
        form_layout.addWidget(self.quantity_input)

        # Discount input field
        # self.discount_label = QLabel("Discount:")
        # self.discount_label.setFont(QFont("Arial", 14))
        # self.discount_input = QLineEdit()
        # self.discount_input.setMinimumWidth(250)
        # form_layout.addWidget(self.discount_label)
        # form_layout.addWidget(self.discount_input)

        # Add Another Product Button
        self.add_another_button = QPushButton("Add  Product")
        self.add_another_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.add_another_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        self.add_another_button.clicked.connect(self.add_product_to_sale)
        form_layout.addWidget(self.add_another_button)

        # Done Button
        self.done_button = QPushButton("Done")
        self.done_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.done_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        self.done_button.clicked.connect(self.generate_receipt)
        form_layout.addWidget(self.done_button)

        # Add form layout to main layout
        main_layout.addLayout(form_layout)


    def populate_name_dropdown(self):
        """Populate the dropdown with product names from the database."""
        query = "SELECT Product_Name FROM tbl_Product WHERE IsDeleted = 0"
            
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
                
                # Add product names to the dropdown
            product_names = [row[0] for row in rows]  # Extract product names from query results
            self.name_dropdown.addItems(product_names)
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load product names: {str(e)}")
    def get_product_price(self, product_name):
        """Fetch the price of a product from the database."""
        query = "SELECT Price FROM tbl_Product WHERE Product_Name = ? AND IsDeleted = 0"
        try:
            cursor.execute(query, (product_name,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the price
            return None  # Return None if product not found
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to fetch price: {str(e)}")
            return None

    def add_product_to_sale(self):
        """Add a product to the current sale (list)."""
        name = self.name_dropdown.currentText()
        try:
            quantity = int(self.quantity_input.text())
            discount = float(0.0)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid quantity and discount values.")
            return

        # Fetch the price and available stock of the selected product from the database
        price = self.get_product_price(name)
        available_stock = self.get_product_stock(name)

        if price is None:
            QMessageBox.warning(self, "Invalid Product", f"Price for product '{name}' not found.")
            return

        # Check if the requested quantity exceeds the available stock
        if quantity > available_stock:
            QMessageBox.warning(self, "Insufficient Stock", f"Cannot sell more than {available_stock} units of '{name}'.")
            return

        # Calculate amount
        amount = (price * quantity) - discount
        product = {
            "name": name,
            "quantity": quantity,
            "rate": price,
            "discount": discount,
            "amount": amount,
            "sale_price": price
        }

        # If it's the first product, generate a new Sale ID
        if not self.sale_id:
            self.sale_id = self.generate_sale_id()

        # Add the product to the products list
        self.products.append(product)

        # Clear the inputs after adding the product
        self.clear_inputs()

        QMessageBox.information(self, "Product Added", f"Product '{name}' has been added to the sale.")

    def get_product_stock(self, product_name):
        """Fetch the available stock for a product from the database."""
        query = "SELECT Quantity FROM tbl_Product WHERE Product_Name = ? AND IsDeleted = 0"
        try:
            cursor.execute(query, (product_name,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the available stock
            return 0  # Return 0 if the product is not found
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to fetch stock: {str(e)}")
            return 0

    def clear_inputs(self):
        """Clear all input fields after adding a product."""
        self.quantity_input.clear()
        # self.discount_input.clear()
        self.name_dropdown.setCurrentIndex(0)

    def generate_sale_id(self):
        """Generate a unique Sale ID"""
        query = "SELECT ISNULL(MAX(Sale_ID), 0) + 1 FROM tbl_Sale"
        cursor.execute(query)
        sale_id = cursor.fetchone()[0]
        return sale_id

    def generate_receipt(self):
        """Generate and show the receipt for all added products."""
        if not self.products:
            QMessageBox.warning(self, "No Products", "Please add at least one product before generating a receipt.")
            return

        # Insert all products into the database under the same Sale ID
        self.insert_sale_data()  # Insert sale and products data at once

        # Show final receipt for all added products
        self.show_receipt()

        # After generating the receipt, clear the sale data
        self.sale_id = None
        self.products.clear()

    def insert_sale_data(self):
        """Insert sale and products data into the database."""
        try:
            # Insert the sale information into tbl_Sale if not already done
            sale_query = "INSERT INTO tbl_Sale (Sale_ID, Sale_Date) VALUES (?, GETDATE())"
            cursor.execute(sale_query, (self.sale_id,))
            cnxn.commit()

            # Insert each product into tbl_Product_And_Sale and update stock in tbl_Product
            for product in self.products:
                product_query = """
                    INSERT INTO tbl_Product_And_Sale (Product_ID, Sale_ID, QuantitySaled, Sale_Price)
                    VALUES (
                    (SELECT Product_ID FROM tbl_Product WHERE Product_Name = ?),
                    ?, ?, ?
                    )
                """
                cursor.execute(product_query, (product["name"], self.sale_id, product["quantity"], product["sale_price"]))

                # Update stock in tbl_Product
                update_stock_query = """
                    UPDATE tbl_Product
                    SET Quantity = Quantity - ?
                    WHERE Product_Name = ?
                """
                cursor.execute(update_stock_query, (product["quantity"], product["name"]))
                cnxn.commit()

        except Exception as e:
            cnxn.rollback()
            QMessageBox.critical(self, "Database Error", f"Failed to insert sale data: {str(e)}")

    def show_receipt(self):
        """Generate and show the final receipt after 'Done' is clicked."""
        receipt_window = ReceiptWindow(self.sale_id, self.products)
        receipt_window.exec_()
class ReceiptWindow(QDialog):
    def __init__(self, sale_id, products):
        super().__init__()
        self.setWindowTitle("Receipt")
        self.setFixedSize(800, 800)
        self.sale_id = sale_id
        self.products = products
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Heading - SEEDBEEJ
        heading_label = QLabel("SEEDBEEJ")
        heading_label.setFont(QFont("Arial", 18, QFont.Bold))
        heading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(heading_label)

        # Dummy Address
        address_label = QLabel("1234 Seedbee St, City, Country")
        address_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(address_label)

        # Dummy Phone Number
        phone_label = QLabel("Phone: +1234567890")
        phone_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(phone_label)

        # Order Number and Date
        order_number = f"Order No: {self.sale_id}"  # Use Sale ID
        date = f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        order_info_label = QLabel(f"{order_number}  {date}")
        order_info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(order_info_label)

        # Table for Product Details
        table = QTableWidget()
        table.setColumnCount(3)  # Columns: Product, Quantity, Amount
        table.setHorizontalHeaderLabels(["Product", "Quantity", "Amount"])

        # Populate table with product data
        table.setRowCount(len(self.products))  # Add a row for each product
        total_amount = 0  # Initialize total amount

        for i, product in enumerate(self.products):
            table.setItem(i, 0, QTableWidgetItem(product["name"]))
            table.setItem(i, 1, QTableWidgetItem(str(product["quantity"])))
            table.setItem(i, 2, QTableWidgetItem(f"{product['amount']:.2f}"))
            total_amount += product["amount"]  # Add product amount to total

        layout.addWidget(table)

        # Display total amount
        total_label = QLabel(f"Total: {total_amount:.2f}")
        total_label.setFont(QFont("Arial", 16, QFont.Bold))
        total_label.setAlignment(Qt.AlignRight)
        total_label.setStyleSheet("padding: 10px;")
        layout.addWidget(total_label)

        # Add a close button
        close_button = QPushButton("Close")
        close_button.setFont(QFont("Arial", 14))
        close_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

