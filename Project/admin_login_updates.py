import pyodbc
import sys
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
    r'DATABASE=db_nursery;'
    r'Trusted_Connection=yes;'
)
cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()
def get_db_connection():
    # Returning global connection and cursor
    return cnxn, cursor
class AlertBox(QWidget):
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
            "Update"
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

        layout.addStretch()
        sidebar.setLayout(layout)

        return sidebar

    def create_main_content(self):
        """Create the main content area (initial view)."""
        main_content = QFrame()
        main_layout = QVBoxLayout(main_content)

        # Title
        table_title = QLabel("Product Inventory")
        table_title.setFont(QFont("Arial", 14, QFont.Bold))
        main_layout.addWidget(table_title)

        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([  # Columns for product inventory
            "Product_ID", "Product_Name", "Type_ID", "Category_ID", "Quantity", "Price", "Shelf_Life"
        ])

        # SQL query to get the data from the product table
        query = "SELECT * FROM tbl_Product"

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

        except pyodbc.Error as e:
            self.show_alert(f"An error occurred: {str(e)}")

        main_layout.addWidget(table)
        return main_content

    def switch_content(self, current, previous):
        """Switch between Admin Dashboard, Product Entry, Update Product, etc."""
        if current is not None:
            if current.text() == "Product Entry":
                new_content = self.create_product_entry_form()
            elif current.text() == "Search":
                new_content = self.create_search_screen()
            elif current.text() == "Shipment Entry":
                new_content = ShipmentForm()
            elif current.text() == "Add Sales":
                new_content = AddSaleForm()  # AddSaleForm needs to be defined
            elif current.text() == "Update":
                new_content = self.create_update_product_form()  # Call the update product form method
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


    def create_product_entry_form(self):
        """Create the product entry form with updated layout and styling."""
        
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)

        # Title
        title = QLabel("Product Entry Form")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title)

        # Fixed radio button section
        radio_layout = QHBoxLayout()
        self.product_radio = QRadioButton("Product")
        self.category_radio = QRadioButton("Category")
        self.subcategory_radio = QRadioButton("Subcategory")
        self.type_radio = QRadioButton("Type")
        radio_layout.addWidget(self.product_radio)
        radio_layout.addWidget(self.category_radio)
        radio_layout.addWidget(self.subcategory_radio)
        radio_layout.addWidget(self.type_radio)

        form_layout.addLayout(radio_layout)

        # Spacer to separate radio buttons and instruction label
        spacer_1 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(spacer_1)

        # Instruction label
        self.instruction_label = QLabel("Select from the above options to make an insertion")
        self.instruction_label.setFont(QFont("Arial", 12))  # Reduced font size
        self.instruction_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.instruction_label)

        # Spacer to add space below the instruction label
        spacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(spacer_2)

        # Dynamic input fields section
        input_layout = QVBoxLayout()
        self.fields = [
            ("Product ID:", self.create_input_field()),
            ("Product Name:", self.create_input_field()),
            ("Type:", self.create_dropdown_from_db("SELECT Type_Name FROM tbl_Type")),
            ("Category:", self.create_dropdown_from_db("SELECT Category_Name FROM tbl_Category")),
            ("Subcategory:", self.create_dropdown_from_db("SELECT Sub_Category_Name FROM tbl_Sub_Category")),
            ("Quantity:", self.create_input_field()),
            ("Price:", self.create_input_field()),
            ("Shelf Life (Months):", self.create_input_field()),
            ("Subcategory Name:", self.create_input_field()),
            ("Category:", self.create_dropdown_from_db("SELECT Category_Name FROM tbl_Category")),
            ("Type:", self.create_dropdown_from_db("SELECT Type_Name FROM tbl_Type")),
            ("Category Name:", self.create_input_field()),
            ("Type:", self.create_dropdown_from_db("SELECT Type_Name FROM tbl_Type")),
            ("Type Name:", self.create_input_field()),
        ]

        # Create placeholders for all fields
        self.input_widgets = []
        for label, widget in self.fields:
            row_layout = QHBoxLayout()
            label_widget = QLabel(label)
            label_widget.setFont(QFont("Arial", 14))
            widget.setFont(QFont("Arial", 14))
            label_widget.setVisible(False)
            widget.setVisible(False)
            row_layout.addWidget(label_widget)
            row_layout.addWidget(widget)
            input_layout.addLayout(row_layout)
            self.input_widgets.append((label_widget, widget))

        form_layout.addLayout(input_layout)

        # Spacer to ensure consistent spacing below
        spacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(spacer_3)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.setFont(QFont("Arial", 14, QFont.Bold))
        submit_button.setStyleSheet("background-color: #4caf50; color: white;")
        submit_button.clicked.connect(self.handle_submission)
        form_layout.addWidget(submit_button)

        # Set default selection for "Product"
        self.product_radio.setChecked(True)
        self.toggle_input_fields()

        # Connect radio button clicks to toggle fields
        self.product_radio.clicked.connect(self.toggle_input_fields)
        self.category_radio.clicked.connect(self.toggle_input_fields)
        self.subcategory_radio.clicked.connect(self.toggle_input_fields)
        self.type_radio.clicked.connect(self.toggle_input_fields)

        return form_frame


    def create_input_field(self):
        """Create an input field."""
        return QLineEdit()

    def create_dropdown_from_db(self, query):
        """Create a dropdown populated from the database."""
        combo_box = QComboBox()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                combo_box.addItem(row[0])
        except pyodbc.Error as e:
            self.show_alert(f"An error occurred while loading dropdown: {str(e)}")
        return combo_box

    def toggle_input_fields(self):
        """Toggle visibility of input fields based on radio button selection."""
        selected_button = self.sender()

        # Hide all fields initially
        for label_widget, widget in self.input_widgets:
            label_widget.setVisible(False)
            widget.setVisible(False)

        # Show fields based on selected radio button
        if self.product_radio.isChecked():
            for i in range(1, 8):  # Show product-related fields
                label_widget, widget = self.input_widgets[i]
                label_widget.setVisible(True)
                widget.setVisible(True)

        elif self.category_radio.isChecked():
            for i in range(11, 13):  # Show category-related fields
                label_widget, widget = self.input_widgets[i]
                label_widget.setVisible(True)
                widget.setVisible(True)

        elif self.subcategory_radio.isChecked():
            for i in range(8, 10):  # Show subcategory-related fields
                label_widget, widget = self.input_widgets[i]
                label_widget.setVisible(True)
                widget.setVisible(True)

        elif self.type_radio.isChecked():
            for i in range(13, 14):  # Show type-related fields
                label_widget, widget = self.input_widgets[i]
                label_widget.setVisible(True)
                widget.setVisible(True)

    def handle_submission(self):
        """Handle form submission."""
        # Extract form values
        product_data = []

        if self.product_radio.isChecked():
            # Iterate over widgets for product-related fields (indexes 1 to 7)
            for label_widget, widget in self.input_widgets[1:8]:  # Slicing the list to get relevant fields
                # Check if widget is a QLineEdit or QComboBox
                if isinstance(widget, QLineEdit):
                    product_data.append(widget.text())  # For text input fields
                elif isinstance(widget, QComboBox):
                    product_data.append(widget.currentText())

            # Ensure the data list is not empty and matches the required number of fields
            if len(product_data) == 7:  # Adjust this number if your fields change
                try:
                    # Extract field values
                    product_name = product_data[0]
                    type_name = product_data[1]
                    category_name = product_data[2]
                    subcategory_name = product_data[3]
                    quantity = int(product_data[4])
                    price = float(product_data[5])
                    shelf_life = int(product_data[6])

                    # Call the stored procedure (Product_ID is omitted as it’s handled by IDENTITY)
                    cursor.execute(
                        "EXEC InsertProductAndLinkSubcategory NULL, ?, ?, ?, ?, ?, ?, ?",
                        (
                            product_name,       # @ProductName
                            type_name,          # @TypeName
                            category_name,      # @CategoryName
                            subcategory_name,   # @SubCategoryName
                            quantity,           # @Quantity
                            price,              # @Price
                            shelf_life          # @ShelfLife
                        )
                    )
                    cnxn.commit()
                    self.show_alert("Product added successfully!")

                except pyodbc.Error as e:
                    # Handle specific SQL errors
                    if "50003" in str(e):  # Check for duplicate product error code
                        self.show_alert("Product already exists in the database.")
                    else:
                        error_message = f"An error occurred while inserting product: {str(e)}"
                        print(error_message)  # Log the error in the console
                        self.show_alert(error_message)  # Display error in the alert box

                except ValueError as e:
                    error_message = f"Validation error: {str(e)}"
                    print(error_message)  # Log the error in the console
                    self.show_alert(error_message)  # Display error in the alert box

            else:
                self.show_alert("Please fill out all the required fields.")

        elif self.category_radio.isChecked():
            # Clear previous data
            product_data = []

            # Iterate over widgets for category-related fields (indexes 11 to 13)
            for label_widget, widget in self.input_widgets[11:13]:  # Slicing the list to get relevant fields
                # Check if widget is a QLineEdit or QComboBox
                if isinstance(widget, QLineEdit):
                    product_data.append(widget.text().strip())  # Trim whitespace for text input fields
                elif isinstance(widget, QComboBox):
                    product_data.append(widget.currentText().strip())  # Trim whitespace for dropdowns

            # Ensure the data list is not empty and matches the required number of fields
            if len(product_data) == 2:  # Adjust this number if your fields change
                try:
                    category_id = 6
                    # Extract field values
                    category_name = product_data[0]
                    type_name = product_data[1]

                    # Validate user inputs
                    if not category_name or not type_name:
                        raise ValueError("Both Category Name and Type Name are required.")

                    # Call the stored procedure
                    cursor.execute(
                        "EXEC InsertCategory ?, ?, ?",
                        (
                            category_id,               # Category_ID is omitted if auto-generated
                            category_name,      # @CategoryName
                            type_name           # @TypeName
                        )
                    )
                    cnxn.commit()
                    self.show_alert("Category added successfully!")

                except pyodbc.Error as e:
                    # Check for duplicate category exception
                    if "Category already exists" in str(e):
                        error_message = "This category already exists in the database."
                    else:
                        error_message = f"An error occurred while inserting category: {str(e)}"
                    
                    print(error_message)  # Log the error in the console
                    self.show_alert(error_message)  # Display error in the alert box

                except ValueError as e:
                    error_message = f"Validation error: {str(e)}"
                    print(error_message)  # Log the error in the console
                    self.show_alert(error_message)  # Display error in the alert box

            else:
                self.show_alert("Please fill out all the required fields.")

        elif self.subcategory_radio.isChecked():
            # Clear previous data
            product_data = []

            # Iterate over widgets for category-related fields (indexes 11 to 13)
            for label_widget, widget in self.input_widgets[8:10]:  # Slicing the list to get relevant fields
                # Check if widget is a QLineEdit or QComboBox
                if isinstance(widget, QLineEdit):
                    product_data.append(widget.text().strip())  # Trim whitespace for text input fields
                elif isinstance(widget, QComboBox):
                    product_data.append(widget.currentText().strip())  # Trim whitespace for dropdowns

            # Ensure the data list is not empty and matches the required number of fields
            if len(product_data) == 2:  # Adjust this number if your fields change
                try:
                    # Extract field values
                    subcategory_id = 5
                    subcategory_name = product_data[0]
                    category_name = product_data[1]

                    # Validate user inputs
                    if not subcategory_name or not category_name :
                        raise ValueError("Both Sub Category Name and Category Name are required.")

                    # Call the stored procedure
                    cursor.execute(
                        "EXEC InsertSubCategory ?, ?, ?",
                        (
                            subcategory_id,               # Category_ID is omitted if auto-generated
                            subcategory_name,
                            category_name                 # @CategoryName
                        )
                    )
                    cnxn.commit()
                    self.show_alert("SubCategory added successfully!")

                except pyodbc.Error as e:
                    # Check for duplicate category exception
                    if "SubCategory already exists" in str(e):
                        error_message = "This subcategory already exists in the database."
                    else:
                        error_message = f"An error occurred while inserting subcategory: {str(e)}"
                    
                    print(error_message)  # Log the error in the console
                    self.show_alert(error_message)  # Display error in the alert box

                except ValueError as e:
                    error_message = f"Validation error: {str(e)}"
                    print(error_message)  # Log the error in the console
                    self.show_alert(error_message)  # Display error in the alert box

            else:
                self.show_alert("Please fill out all the required fields.")

        elif self.type_radio.isChecked():
            # Clear previous data
            product_data = []

            # Iterate over widgets for category-related fields (indexes 11 to 13)
            for label_widget, widget in self.input_widgets[13:14]:  # Slicing the list to get relevant fields
                # Check if widget is a QLineEdit or QComboBox
                if isinstance(widget, QLineEdit):
                    product_data.append(widget.text().strip())  # Trim whitespace for text input fields
                elif isinstance(widget, QComboBox):
                    product_data.append(widget.currentText().strip())  # Trim whitespace for dropdowns

            # Ensure the data list is not empty and matches the required number of fields
            if len(product_data) == 1:  # Adjust this number if your fields change
                try:
                    # Extract field values
                    type_id = 5
                    type_name = product_data[0]

                    # Validate user inputs
                    if not type_name :
                        raise ValueError("Type Name is required.")

                    # Call the stored procedure
                    cursor.execute(
                        "EXEC InsertType ?, ?",
                        (
                            type_id,
                            type_name
                        )
                    )
                    cnxn.commit()
                    self.show_alert("Type added successfully!")

                except pyodbc.Error as e:
                    # Check for duplicate type exception
                    if "Type already exists" in str(e):
                        error_message = "This type already exists in the database."
                    else:
                        error_message = f"An error occurred while inserting type: {str(e)}"
                    
                    print(error_message)  # Log the error in the console
                    self.show_alert(error_message)  # Display error in the alert box

                except ValueError as e:
                    error_message = f"Validation error: {str(e)}"
                    print(error_message)  # Log the error in the console
                    self.show_alert(error_message)  # Display error in the alert box

            else:
                self.show_alert("Please fill out the required field.")

    def create_search_screen(self):
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
        self.product_name_radio = QRadioButton("Product Name")
        self.type_radio = QRadioButton("Type")
        self.category_radio = QRadioButton("Category")
        self.subcategory_radio = QRadioButton("Subcategory")
        self.quantity_radio = QRadioButton("Quantity")
        self.expiry_date_radio = QRadioButton("Expiry Date")

        self.product_radio = QRadioButton("Product")
        self.shipment_date_radio = QRadioButton("Shipment Date")
        self.sale_date_radio = QRadioButton("Sale Date")

        self.product_name_radio.setChecked(True)  # Default selection

        # Function to update criteria based on search option
        def update_criteria():
            for i in reversed(range(criteria_layout.count())):
                criteria_layout.itemAt(i).widget().setParent(None)

            if search_options.currentText() == "Search Product":
                criteria_layout.addWidget(self.product_name_radio)
                criteria_layout.addWidget(self.type_radio)
                criteria_layout.addWidget(self.category_radio)
                criteria_layout.addWidget(self.subcategory_radio)
                criteria_layout.addWidget(self.quantity_radio)
                criteria_layout.addWidget(self.expiry_date_radio)
            elif search_options.currentText() == "Search Shipment":
                criteria_layout.addWidget(self.product_radio)
                criteria_layout.addWidget(self.shipment_date_radio)
            elif search_options.currentText() == "Search Sale":
                criteria_layout.addWidget(self.product_radio)
                criteria_layout.addWidget(self.sale_date_radio)

        search_options.currentIndexChanged.connect(update_criteria)
        update_criteria()

        search_layout.addLayout(criteria_layout)

        # Search input field
        search_input = QLineEdit()
        search_input.setPlaceholderText("Enter product name to search")
        search_layout.addWidget(search_input)

        # Update placeholder text based on selected radio button
        def update_placeholder():
            if self.product_name_radio.isChecked():
                search_input.setPlaceholderText("Enter product name to search")
            elif self.type_radio.isChecked():
                search_input.setPlaceholderText("Enter type to search")
            elif self.category_radio.isChecked():
                search_input.setPlaceholderText("Enter category to search")
            elif self.subcategory_radio.isChecked():
                search_input.setPlaceholderText("Enter subcategory to search")
            elif self.quantity_radio.isChecked():
                search_input.setPlaceholderText("Enter quantity to search")
            elif self.expiry_date_radio.isChecked():
                search_input.setPlaceholderText("Enter expiry date to search")
            elif self.product_radio.isChecked():
                search_input.setPlaceholderText("Enter product to search")
            elif self.shipment_date_radio.isChecked():
                search_input.setPlaceholderText("Enter shipment date to search")
            elif self.sale_date_radio.isChecked():
                search_input.setPlaceholderText("Enter sale date to search")

        self.product_name_radio.toggled.connect(update_placeholder)
        self.type_radio.toggled.connect(update_placeholder)
        self.category_radio.toggled.connect(update_placeholder)
        self.subcategory_radio.toggled.connect(update_placeholder)
        self.quantity_radio.toggled.connect(update_placeholder)
        self.expiry_date_radio.toggled.connect(update_placeholder)
        self.product_radio.toggled.connect(update_placeholder)
        self.shipment_date_radio.toggled.connect(update_placeholder)
        self.sale_date_radio.toggled.connect(update_placeholder)

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
            search_query = search_input.text()
            if search_options.currentText() == "Search Product":
                if self.product_name_radio.isChecked():
                    query = "SELECT * FROM tbl_Product WHERE Product_Name LIKE ?"
                elif self.type_radio.isChecked():
                    query = "SELECT * FROM tbl_Product WHERE Type_ID LIKE ?"
                elif self.category_radio.isChecked():
                    query = "SELECT * FROM tbl_Product WHERE Category_ID LIKE ?"
                elif self.subcategory_radio.isChecked():
                    query = "SELECT * FROM tbl_Product WHERE Subcategory_ID LIKE ?"
                elif self.quantity_radio.isChecked():
                    query = "SELECT * FROM tbl_Product WHERE Quantity LIKE ?"
                elif self.expiry_date_radio.isChecked():
                    query = "SELECT * FROM tbl_Product WHERE Shelf_Life LIKE ?"
                else:
                    query = ""  # Fallback
            elif search_options.currentText() == "Search Shipment":
                if self.product_radio.isChecked():
                    query = "SELECT * FROM tbl_Shipment WHERE Product LIKE ?"
                elif self.shipment_date_radio.isChecked():
                    query = "SELECT * FROM tbl_Shipment WHERE Shipment_Date LIKE ?"
                else:
                    query = ""  # Fallback
            elif search_options.currentText() == "Search Sale":
                if self.product_radio.isChecked():
                    query = "SELECT * FROM tbl_Sale WHERE Product LIKE ?"
                elif self.sale_date_radio.isChecked():
                    query = "SELECT * FROM tbl_Sale WHERE Sale_Date LIKE ?"
                else:
                    query = ""  # Fallback

            if query:
                cursor.execute(query, f"%{search_query}%")
                rows = cursor.fetchall()
                result_table.setRowCount(len(rows))
                for row_index, row in enumerate(rows):
                    for col_index, value in enumerate(row):
                        result_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        # Clear input and results
        def clear_data():
            search_input.clear()
            result_table.setRowCount(0)

        search_button.clicked.connect(perform_search)
        clear_button.clicked.connect(clear_data)

        return search_frame

    def show_alert(self, message):
        alert = AlertBox(message, self)
        alert.show()

    def logout(self):
        """Logout action"""
        self.close()
        app.quit()

    def create_update_product_form(self):
        """Create the form for updating product information."""
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)

    # Title
        title = QLabel("Update Product")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        form_layout.addWidget(title)

    # Dropdown for product names
        self.product_name_dropdown = self.create_dropdown_from_db("SELECT Product_Name FROM tbl_Product")
        self.product_name_dropdown.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.product_name_dropdown)

    # Input fields for price and shelf life
        self.price_label = QLabel("Price:")
        self.price_label.setFont(QFont("Arial", 14))
        self.price_input = QLineEdit()
        self.price_input.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.price_label)
        form_layout.addWidget(self.price_input)

        self.shelf_life_label = QLabel("Shelf Life (Months):")
        self.shelf_life_label.setFont(QFont("Arial", 14))
        self.shelf_life_input = QLineEdit()
        self.shelf_life_input.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.shelf_life_label)
        form_layout.addWidget(self.shelf_life_input)

    # Button to fetch product details
        fetch_button = QPushButton("Fetch Details")
        fetch_button.setFont(QFont("Arial", 14, QFont.Bold))
        fetch_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        fetch_button.clicked.connect(self.fetch_product_details)
        form_layout.addWidget(fetch_button)

        # Submit button to update product
        update_button = QPushButton("Update Product")
        update_button.setFont(QFont("Arial", 14, QFont.Bold))
        update_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        update_button.clicked.connect(self.update_product)
        form_layout.addWidget(update_button)

        return form_frame
    
    def fetch_product_details(self):
        """Fetch product details based on the selected product."""
        product_name = self.product_name_dropdown.currentText()
        if not product_name:
            self.show_alert("Please select a product.")
            return
        # Query to get the current details for the selected product
        query = "SELECT Price, Shelf_Life FROM tbl_Product WHERE Product_Name = ?"
        
        try:
            cursor.execute(query, (product_name,))
            row = cursor.fetchone()
            if row:
                # Populate the fields with the current product details
                self.price_input.setText(str(row[0]))
                self.shelf_life_input.setText(str(row[1]))
            else:
                self.show_alert("Product not found.")
        except pyodbc.Error as e:
            self.show_alert(f"An error occurred: {str(e)}")

    def update_product(self):
        """Update the selected product's price and shelf life."""
        product_name = self.product_name_dropdown.currentText()
        price = self.price_input.text()
        shelf_life = self.shelf_life_input.text()

        if not price or not shelf_life:
            self.show_alert("Please fill in both fields.")
            return

        try:
            # Update the product details in the database
            query = """UPDATE tbl_Product
                    SET Price = ?, Shelf_Life = ?
                    WHERE Product_Name = ?"""
            cursor.execute(query, (price, shelf_life, product_name))
            cnxn.commit()
            self.show_alert("Updated successfully!")
        except pyodbc.Error as e:
            self.show_alert(f"An error occurred: {str(e)}")

    def show_alert(self, message):
        alert = AlertBox(message, self)
        alert.show()
        
        

    


  #SHIPMENT FRONTEND-----------------------------------------------      
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ShipmentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shipment Entry")
        self.shipments = []  # List to store all the added shipments temporarily
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

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
        self.populate_name_dropdown()  # Populate the dropdown from the database or predefined list
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
        self.done_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        self.done_button.clicked.connect(self.add_shipment)
        main_layout.addWidget(self.done_button)

        # Add Another Shipment Button
        self.add_another_button = QPushButton("Add Another Shipment")
        self.add_another_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.add_another_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        self.add_another_button.clicked.connect(self.add_to_shipment_list)
        main_layout.addWidget(self.add_another_button)

        # Set the overall layout for the widget
        self.setLayout(main_layout)

    def populate_name_dropdown(self):
        """Populate the dropdown with product names from the database."""
        query = "SELECT Product_Name FROM tbl_Product"
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Add product names to the dropdown
            product_names = [row[0] for row in rows]  # Extract product names from query results
            self.name_dropdown.addItems(product_names)
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load product names: {str(e)}")

    def add_shipment(self):
        """Handle the 'Done' button click - Add all the shipments to the database."""
        # Ensure the last product is added before proceeding
        self.add_to_shipment_list()

        # Now process all shipments in the list
        if not self.shipments:
            QMessageBox.warning(self, "No Shipments", "No products were added to the shipment.")
            return

        try:
            # Generate the next Purchase_ID
            get_max_id_query = "SELECT ISNULL(MAX(Purchase_ID), 0) + 1 FROM tbl_Purchase"
            cursor.execute(get_max_id_query)
            purchase_id = cursor.fetchone()[0]

            # Insert a new Purchase record into tbl_Purchase
            purchase_query = "INSERT INTO tbl_Purchase (Purchase_ID, Purchase_Date) VALUES (?, GETDATE())"
            cursor.execute(purchase_query, (purchase_id,))
            cnxn.commit()

            # Insert the products into the tbl_Product_And_Purchase
            for shipment in self.shipments:
                product_name, price, quantity = shipment
                product_query = "SELECT Product_ID FROM tbl_Product WHERE Product_Name = ?"
                cursor.execute(product_query, (product_name,))
                product_row = cursor.fetchone()
                if not product_row:
                    QMessageBox.warning(self, "Product Error", f"Product {product_name} not found.")
                    return
                product_id = product_row[0]

                insert_purchase_query = """
                    INSERT INTO tbl_Product_And_Purchase 
                    (Product_ID, Purchase_ID, QuantityPurchased, Purchasing_Price, Selling_Price) 
                    VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(insert_purchase_query, (product_id, purchase_id, quantity, price, price))
                cnxn.commit()

                # Update the product quantity in tbl_Product
                update_product_query = """
                    UPDATE tbl_Product
                    SET Quantity = Quantity + ?
                    WHERE Product_ID = ?
                """
                cursor.execute(update_product_query, (quantity, product_id))
                cnxn.commit()

            QMessageBox.information(self, "Success", "All Shipments Added and Products Updated Successfully!")

            # Clear the inputs and the temporary shipment list
            self.clear_inputs()

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price must be a valid number and quantity must be an integer.")
        except Exception as e:
            cnxn.rollback()  # Rollback any changes if an error occurs
            QMessageBox.critical(self, "Error", f"Failed to add shipment: {str(e)}")

    def add_to_shipment_list(self):
        """Add a shipment to the temporary shipment list."""
        name = self.name_dropdown.currentText()
        price = self.price_input.text()
        quantity = self.quantity_input.text()

        # Ensure inputs are valid before adding to the list
        if not name or not price or not quantity:
            return

        price = float(price)
        quantity = int(quantity)

        # Add product to the temporary shipment list
        self.shipments.append((name, price, quantity))

        # Clear input fields after adding to the list (if Add Another Shipment is clicked)
        if self.sender() == self.add_another_button:
            self.clear_inputs()

    def clear_inputs(self):
        """Clear all input fields for adding another shipment."""
        self.price_input.clear()
        self.quantity_input.clear()
        self.name_dropdown.setCurrentIndex(0)


#ADDING SALE FORM ------------------------------------------------------------
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from datetime import datetime
import pyodbc  # Assuming you're using pyodbc for database connectivity




if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = AdminLoginPage()
    login_window.show()
    sys.exit(app.exec_())