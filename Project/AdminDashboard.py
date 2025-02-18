import pyodbc
import sys
from ShipmentForm import ShipmentForm
from create_product_entry_form import create_product_entry_form
from create_search_screen import create_search_screen
from AddSaleForm import AddSaleForm
from create_update_product_form import create_update_product_form
from DeleteProductForm import DeleteProductForm
from StatisticsView import StatisticsView


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
class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard - Gardening Shop")
        self.setGeometry(100, 100, 1200, 700)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout(self)

        # Sidebar (left menu)
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Main content area (initially shows dashboard)
        self.main_content = QFrame()
        self.main_content.setLayout(QVBoxLayout())
        main_layout.addWidget(self.main_content)

        self.setLayout(main_layout)

        # Initialize with the dashboard view
        self.switch_content(self.menu.item(0), None)

    def create_sidebar(self):
        """Create the left sidebar.""" 
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #e8f5e9; border-right: 1px solid #bdbdbd;")
        sidebar.setFixedWidth(250)

        layout = QVBoxLayout()

        # Logo or title
        title = QLabel("Gardening Shop")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #1b5e20;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Menu buttons
        buttons = [
            "Dashboard",
            "Product Entry",
            "Search",
            "Shipment Entry",
            "Add Sales",
            "Update",
            "Delete",
            "View Statistics"
        ]
        self.menu = QListWidget()
        for button in buttons:
            self.menu.addItem(button)
        self.menu.setStyleSheet(""" 
            QListWidget::item {
                padding: 10px;
                border: none;
            }
            QListWidget::item:selected {
                background-color: #4caf50;
                color: white;
            }
        """)
        self.menu.currentItemChanged.connect(self.switch_content)
        layout.addWidget(self.menu)

        # Footer with user info
        user_info = QLabel("Logged In As\nAdmin")
        user_info.setFont(QFont("Arial", 12))
        user_info.setStyleSheet("color: #1b5e20;")
        user_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_info)

        logout_button = QPushButton("LOG OUT")
        logout_button.setFont(QFont("Arial", 12, QFont.Bold))
        logout_button.setStyleSheet(
            "background-color: #4caf50; color: white; padding: 10px; border-radius: 5px; border: none;"
        )
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button, alignment=Qt.AlignCenter)
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button, alignment=Qt.AlignCenter)
        layout.addStretch()
        sidebar.setLayout(layout)

        return sidebar
    def logout(self):
        """Logout action"""
        self.close()
        app.quit()

    def create_main_content(self):
        """Create the main content area (initial view)."""
        main_content = QFrame()
        main_layout = QVBoxLayout(main_content)

        # Title
        table_title = QLabel("Product Inventory")
        table_title.setFont(QFont("Arial", 14, QFont.Bold))
        main_layout.addWidget(table_title)

        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels([  # Columns for product inventory
            "Product_ID", "Product_Name", "Type_Name", "Category_Name", "SubCategory", "In Stock", "Price", "Shelf_Life"
        ])

        # SQL query to get the data from the product table
        query = """
        SELECT 
            p.Product_ID,
            p.Product_Name,
            (SELECT t.Type_Name 
            FROM tbl_Type t 
            WHERE t.Type_ID = p.Type_ID) AS Type_Name,
            (SELECT c.Category_Name 
            FROM tbl_Category c 
            WHERE c.Category_ID = p.Category_ID) AS Category_Name,
            STUFF((
                SELECT ',' + s.Sub_Category_Name
                FROM tbl_Product_And_Sub_Category ps
                JOIN tbl_Sub_Category s ON s.Sub_Category_ID = ps.Sub_Category_ID
                WHERE ps.Product_ID = p.Product_ID
                FOR XML PATH('')
            ), 1, 1, '') AS Subcategory_Name,
            p.Quantity,
            p.Price,
            p.Shelf_Life
        FROM 
            tbl_Product p
        WHERE
            p.IsDeleted = 0
        """

        try:
            # Execute the query
            cursor.execute(query)
            rows = cursor.fetchall()

            # Set the number of rows dynamically
            table.setRowCount(len(rows))
            table.verticalHeader().setVisible(False)

            # Populate the table with database data
            for row_index, row in enumerate(rows):
                for col_index, value in enumerate(row):
                    table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

                # Check if quantity is less than 10 and set row color
                quantity = row[5]  # Assuming Quantity is at index 5 (6th column)
                if quantity < 10:
                    for col_index in range(table.columnCount()):
                        item = table.item(row_index, col_index)
                        item.setBackground(QColor(144, 238, 144))  # Set background to red (tomato color)

            # Set custom column widths
            table.setColumnWidth(1, 240)  # Product_Name
            table.setColumnWidth(2, 240)  # Type_Name
            table.setColumnWidth(3, 240)  # Category_Name
            table.setColumnWidth(4, 300)  # Subcategory_Name

        except pyodbc.Error as e:
            self.show_alert(f"An error occurred: {str(e)}")

        main_layout.addWidget(table)

        # Add "Product History" button at the bottom of the Product Inventory screen
        product_history_button = QPushButton("Price History")
        product_history_button.setFont(QFont("Arial", 12, QFont.Bold))
        product_history_button.setStyleSheet(
            "background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;"
        )
        product_history_button.clicked.connect(self.show_product_history)
        main_layout.addWidget(product_history_button, alignment=Qt.AlignBottom | Qt.AlignRight)

        return main_content


 
    def show_product_history(self):
        """Handle Product History button click."""
        # Clear the main content area
        layout = self.main_content.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Create new layout for product history view
        history_layout = QVBoxLayout()

        # Label
        name_label = QLabel("Select Product:")
        name_label.setFont(QFont("Arial", 16, QFont.Bold))
        history_layout.addWidget(name_label)

        # Dropdown
        self.product_dropdown = QComboBox()
        self.product_dropdown.setFont(QFont("Arial", 12))

        # Populate dropdown with product names from the database
        try:
            query = "SELECT Product_Name FROM tbl_Product"
            cursor.execute(query)
            products = cursor.fetchall()
            self.product_dropdown.addItems([product[0] for product in products])
        except pyodbc.Error as e:
            self.show_alert(f"An error occurred while fetching product names: {str(e)}")
            return

        self.product_dropdown.currentTextChanged.connect(self.display_product_history)
        history_layout.addWidget(self.product_dropdown)

        # Table to show product history
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)  # Assuming PriceHistory has 4 columns
        self.history_table.setHorizontalHeaderLabels(["Product_ID", "Date", "Price"])

        history_layout.addWidget(self.history_table)

        # Back button
        back_button = QPushButton("Back to Inventory")
        back_button.setFont(QFont("Arial", 12, QFont.Bold))
        back_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        back_button.clicked.connect(self.show_product_history)  # Connect to method to go back
        history_layout.addWidget(back_button, alignment=Qt.AlignRight)

        # Set the new layout to the main content
        container = QFrame()
        container.setLayout(history_layout)
        layout.addWidget(container)
        
        def show_product_inventory(self):
            """Recreate the Product Inventory view."""
            layout = self.main_content.layout()
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            # Add the product inventory view
            inventory_content = self.create_main_content()
            layout.addWidget(inventory_content)


    def display_product_history(self, product_name):
        """Fetch and display the price history of the selected product."""
        if not product_name:
            self.history_table.setRowCount(0)
            return

        # Query to get the Product_ID of the selected product
        query = "SELECT Product_ID FROM tbl_Product WHERE Product_Name = ?"
        try:
            cursor.execute(query, (product_name,))
            product = cursor.fetchone()

            if product:
                product_id = product[0]

                # Query to get the price history for this Product_ID
                history_query = """
                SELECT Updation_Date, Updated_Price
                FROM tbl_pricehistory
                WHERE Product_ID = ?
                ORDER BY Updation_Date DESC
                """
                cursor.execute(history_query, (product_id,))
                rows = cursor.fetchall()

                # Set the number of rows in the table
                self.history_table.setRowCount(len(rows))

                # Populate the table with data
                for row_index, row in enumerate(rows):
                    self.history_table.setItem(row_index, 0, QTableWidgetItem(str(product_id)))  # Product_ID
                    self.history_table.setItem(row_index, 1, QTableWidgetItem(str(row[0])))  # Updation_Date
                    self.history_table.setItem(row_index, 2, QTableWidgetItem(str(row[1])))  # Updated_Price
            else:
                self.show_alert("No product found.")
                self.history_table.setRowCount(0)

        except pyodbc.Error as e:
            self.show_alert(f"An error occurred while fetching price history: {str(e)}")


    def switch_content(self, current, previous):
        """Switch between Admin Dashboard, Product Entry, Update Product, etc."""
        if current is not None:
            if current.text() == "Product Entry":
                new_content = create_product_entry_form.create_product_entry_form()
            elif current.text() == "Search":
                new_content = create_search_screen.create_search_screen()
            elif current.text() == "Shipment Entry":
                new_content = ShipmentForm()
            elif current.text() == "Add Sales":
                new_content = AddSaleForm()  # AddSaleForm needs to be defined
            elif current.text() == "Update":
                new_content = create_update_product_form.create_update_product_form()  # Call the update product form method
                # update_form_instance = create_update_product_form()
            elif current.text() == "Delete":
                new_content = DeleteProductForm()
            elif current.text() == "View Statistics":
                new_content = StatisticsView()     
                
            else:
                new_content = self.create_main_content()

            # Clear the existing layout
            layout = self.main_content.layout()
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

        # Add new content to the layout
        layout.addWidget(new_content)