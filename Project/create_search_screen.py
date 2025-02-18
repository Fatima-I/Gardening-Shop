import pyodbc
import sys

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
class create_search_screen(QWidget):

    @staticmethod
    def create_search_screen():
        search_frame = QFrame()
        search_layout = QVBoxLayout(search_frame)

        title = QLabel("Search")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        search_layout.addWidget(title)

        # Dropdown for search options
        search_options = QComboBox()
        search_options.addItems(["Search Product", "Search Shipment", "Search Sale"])
        search_layout.addWidget(search_options)

        # Label for search by
        search_by_label = QLabel("Search by:")
        search_by_label.setFont(QFont("Arial", 12))
        search_layout.addWidget(search_by_label)

        # Radio Buttons for search criteria
        criteria_layout = QHBoxLayout()
        product_name_radio = QRadioButton("Product Name")
        type_radio = QRadioButton("Type")
        category_radio = QRadioButton("Category")
        subcategory_radio = QRadioButton("Subcategory")
        quantity_radio = QRadioButton("Quantity")
        expiry_date_radio = QRadioButton("Expiry Date")

        product_radio = QRadioButton("Product")
        shipment_date_radio = QRadioButton("Shipment Date")
        sale_date_radio = QRadioButton("Sale Date")

        product_name_radio.setChecked(True)  # Default selection

        # Function to update criteria based on search option
        def update_criteria():
            for i in reversed(range(criteria_layout.count())):
                criteria_layout.itemAt(i).widget().setParent(None)

            if search_options.currentText() == "Search Product":
                criteria_layout.addWidget(product_name_radio)
                criteria_layout.addWidget(type_radio)
                criteria_layout.addWidget(category_radio)
                criteria_layout.addWidget(subcategory_radio)
                criteria_layout.addWidget(quantity_radio)
                criteria_layout.addWidget(expiry_date_radio)
            elif search_options.currentText() == "Search Shipment":
                criteria_layout.addWidget(product_radio)
                criteria_layout.addWidget(shipment_date_radio)
            elif search_options.currentText() == "Search Sale":
                criteria_layout.addWidget(product_radio)
                criteria_layout.addWidget(sale_date_radio)

        search_options.currentIndexChanged.connect(update_criteria)
        update_criteria()

        search_layout.addLayout(criteria_layout)

        # Search input field
        search_input = QLineEdit()
        search_input.setPlaceholderText("Enter product name to search")
        search_layout.addWidget(search_input)

        # Update placeholder text based on selected radio button
        def update_placeholder():
            # First, check if the search option is "Search Shipment" or "Search Sale"
            if search_options.currentText() == "Search Shipment":
                # Update the placeholder based on radio button selection for Search Shipment
                if product_radio.isChecked():
                    search_input.setPlaceholderText("Enter product name to search")
                elif shipment_date_radio.isChecked():
                    search_input.setPlaceholderText("Enter YYYY Or YYYY-MM Or YYYY-MM-DD")
            elif search_options.currentText() == "Search Sale":
                # Update the placeholder based on radio button selection for Search Sale
                if product_radio.isChecked():
                    search_input.setPlaceholderText("Enter product name to search")
                elif sale_date_radio.isChecked():
                    search_input.setPlaceholderText("Enter YYYY Or YYYY-MM Or YYYY-MM-DD")
            else:
                # Handle the placeholder for product search or other search options
                if product_name_radio.isChecked():
                    search_input.setPlaceholderText("Enter product name to search")
                elif type_radio.isChecked():
                    search_input.setPlaceholderText("Enter type to search")
                elif category_radio.isChecked():
                    search_input.setPlaceholderText("Enter category to search")
                elif subcategory_radio.isChecked():
                    search_input.setPlaceholderText("Enter subcategory to search")
                elif quantity_radio.isChecked():
                    search_input.setPlaceholderText("Enter quantity to search")
                elif expiry_date_radio.isChecked():
                    search_input.setPlaceholderText("Enter YYYY Or YYYY-MM Or YYYY-MM-DD")

        # Connect each radio button's toggled signal to update the placeholder
        product_name_radio.toggled.connect(update_placeholder)
        type_radio.toggled.connect(update_placeholder)
        category_radio.toggled.connect(update_placeholder)
        subcategory_radio.toggled.connect(update_placeholder)
        quantity_radio.toggled.connect(update_placeholder)
        expiry_date_radio.toggled.connect(update_placeholder)
        product_radio.toggled.connect(update_placeholder)
        shipment_date_radio.toggled.connect(update_placeholder)
        sale_date_radio.toggled.connect(update_placeholder)

        # Connect search_options change to update the placeholder
        search_options.currentTextChanged.connect(update_placeholder)

        # Initially call update_placeholder to set the correct placeholder based on the initial conditions
        update_placeholder()



        # Buttons for search and clear
        button_layout = QHBoxLayout()

        search_button = QPushButton("Search")
        search_button.setFont(QFont("Arial", 14))
        search_button.setStyleSheet("background-color: #4caf50; color: white;")
        button_layout.addWidget(search_button)

        clear_button = QPushButton("Clear")
        clear_button.setFont(QFont("Arial", 14))
        clear_button.setStyleSheet("background-color: #4caf50; color: white;")
        button_layout.addWidget(clear_button)

        search_layout.addLayout(button_layout)

        # Results table
        result_table = QTableWidget()
        result_table.setColumnCount(7)
        result_table.setHorizontalHeaderLabels([
            "Product_ID", "Product_Name", "Type_ID", "Category_ID", "Quantity", "Price", "Shelf_Life"
        ])
        search_layout.addWidget(result_table)

        # Perform search based on selected criteria
        def perform_search():
            query = ""  # Initialize query to an empty string

            search_query = search_input.text()  # Get user input
            if not search_query.strip():
                QMessageBox.warning(None, "Search Error", "Please enter a search query.")
                return

            search_type = ""  # To store the search column type

            # Set the search type based on the selected radio buttons
            if product_name_radio.isChecked():
                search_type = 'Product_Name'
            elif type_radio.isChecked():
                search_type = 'Type_Name'
            elif category_radio.isChecked():
                search_type = 'Category_Name'
            elif subcategory_radio.isChecked():
                search_type = 'Subcategory_Name'  # Use Subcategory_Name for subcategory search
            elif quantity_radio.isChecked():
                search_type = 'Quantity'

            try:
                # Assuming the connection to the database is already established
                cursor = cnxn.cursor()

                if expiry_date_radio.isChecked():
                    rows=[]
                    try:
                        # Call the stored procedure for fetching product expiry details
                        cursor.execute("EXEC GetProductExpiryDetails @SearchQuery = ?", (search_query,))
                        rows = cursor.fetchall()

                        # If no rows are returned, notify the user
                        if not rows:
                            QMessageBox.information(None, "No Results", "No data found for the given expiry date query.")
                            return

                        # Configure the result table for the query output
                        result_table.setRowCount(len(rows))
                        result_table.setColumnCount(4)  # 4 columns: Product ID, Product Name, Quantity, Expiry Date
                        result_table.setHorizontalHeaderLabels([
                            "Product ID", "Product Name", "Quantity", "Expiry Date"
                        ])

                        # Populate the result table with query results
                        for row_index, row in enumerate(rows):
                            for col_index, value in enumerate(row):
                                result_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

                    except Exception as e:
                        # Handle any exceptions that occur
                        QMessageBox.warning(None, "Database Error", f"An error occurred: {str(e)}")

                else:
                    # Handle other searches
                    if not search_type:  # Ensure a valid search type is selected
                        QMessageBox.warning(None, "Search Error", "Please select a valid search type.")
                        return

                    cursor.execute("EXEC SearchProduct ?, ?", (search_query, search_type))
                    rows = cursor.fetchall()

                    # Configure result table for general search
                    result_table.setRowCount(len(rows))
                    result_table.setColumnCount(7)  # Product ID, Name, Type, etc.
                    result_table.setHorizontalHeaderLabels([
                        "Product ID", "Product Name", "Type Name", "Category Name", 
                        "Quantity", "Shelf Life", "Subcategory"
                    ])

                # Populate the result table
                for row_index, row in enumerate(rows):
                    for col_index, value in enumerate(row):
                        result_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

                result_table.setColumnWidth(0, 100)  # Product ID column
                result_table.setColumnWidth(1, 240)  # Product Name column
                result_table.setColumnWidth(2, 240)  # Type Name column
                result_table.setColumnWidth(3, 240)  # Category Name column
                result_table.setColumnWidth(4, 100)  # Quantity column
                result_table.setColumnWidth(5, 100)  # Shelf Life column
                result_table.setColumnWidth(6, 300)  # SubCategory column

            except Exception as e:
                QMessageBox.warning(None, "Database Error", f"An error occurred: {str(e)}")

            # Additional handling for other search types
            if search_options.currentText() == "Search Shipment":
                try:
                    search_type = ""  # Initialize search type
                    search_value = search_input.text().strip()  # Get and sanitize user input
                    
                    # Check which radio button is selected and validate the input
                    if product_radio.isChecked():
                        search_type = "Product"
                        if not search_value:
                            raise ValueError("Product Name cannot be empty. Please provide a valid input.")
                    elif shipment_date_radio.isChecked():
                        search_type = "Shipment Date"
                        if not search_value:
                            raise ValueError("Shipment Date cannot be empty. Please provide a valid input.")
                    else:
                        raise ValueError("Please select either 'Product' or 'Shipment Date'.")

                    # Prepare to call the stored procedure
                    cursor = cnxn.cursor()
                    cursor.execute("EXEC SearchShipment @SearchType = ?, @SearchValue = ?", (search_type, search_value))
                    
                    # Fetch the results
                    rows = cursor.fetchall()
                    
                    # Check if no results were found
                    if not rows:
                        QMessageBox.information(None, "No Results", "No data found for the given input.")
                        return

                    # Set up the result table with appropriate headers
                    result_table.setRowCount(len(rows))
                    result_table.setColumnCount(6)  # 6 columns for Purchase ID, Purchase Date, Product Name, Quantity, Price, Total
                    result_table.setHorizontalHeaderLabels([
                        "Purchase ID", "Purchase Date", "Product Name", 
                        "Quantity Purchased", "Purchase Price", "Total"
                    ])

                    # Populate the result table
                    for row_index, row in enumerate(rows):
                        for col_index, value in enumerate(row):
                            result_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

                except pyodbc.Error as db_error:
                    QMessageBox.warning(None, "Database Error", f"A database error occurred: {str(db_error)}")
                except ValueError as ve:
                    QMessageBox.warning(None, "Input Error", str(ve))
                except Exception as ex:
                    QMessageBox.warning(None, "Unexpected Error", f"An unexpected error occurred: {str(ex)}")


            elif search_options.currentText() == "Search Sale":
                try:
                    # Check for the selected radio button and build query
                    if product_radio.isChecked():
                        search_type = "Product"
                        query = "EXEC SearchSale @SearchType = ?, @SearchValue = ?"
                        cursor.execute(query, (search_type, search_query))
                    elif sale_date_radio.isChecked():
                        search_type = "Sale Date"
                        query = "EXEC SearchSale @SearchType = ?, @SearchValue = ?"
                        cursor.execute(query, (search_type, search_query))
                    else:
                        raise ValueError("Please select either 'Product' or 'Sale Date'.")

                    # Fetch the results
                    rows = cursor.fetchall()
                    
                    # Check if no results were found
                    if not rows:
                        QMessageBox.information(None, "No Results", "No data found for the given input.")
                        return

                    # Set up the result table with appropriate headers
                    result_table.setRowCount(len(rows))
                    result_table.setColumnCount(6)  # 6 columns for Sale ID, Sale Date, Product Name, Quantity Sold, Sale Price, Total
                    result_table.setHorizontalHeaderLabels([
                        "Sale ID", "Sale Date", "Product Name", 
                        "Quantity Sold", "Sale Price", "Total"
                    ])

                    # Populate the result table
                    for row_index, row in enumerate(rows):
                        for col_index, value in enumerate(row):
                            result_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

                except pyodbc.Error as db_error:
                    QMessageBox.warning(None, "Database Error", f"A database error occurred: {str(db_error)}")
                except ValueError as ve:
                    QMessageBox.warning(None, "Input Error", str(ve))
                except Exception as ex:
                    QMessageBox.warning(None, "Unexpected Error", f"An unexpected error occurred: {str(ex)}")

        # Clear input and results
        def clear_data():
            search_input.clear()
            result_table.setRowCount(0)

        search_button.clicked.connect(perform_search)
        clear_button.clicked.connect(clear_data)

        return search_frame
