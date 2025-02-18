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

class create_product_entry_form(QWidget):
    @staticmethod
    def create_product_entry_form():
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
        create_product_entry_form.product_radio = QRadioButton("Product")
        create_product_entry_form.category_radio = QRadioButton("Category")
        create_product_entry_form.subcategory_radio = QRadioButton("Subcategory")
        create_product_entry_form.type_radio = QRadioButton("Type")
        radio_layout.addWidget(create_product_entry_form.product_radio)
        radio_layout.addWidget(create_product_entry_form.category_radio)
        radio_layout.addWidget(create_product_entry_form.subcategory_radio)
        radio_layout.addWidget(create_product_entry_form.type_radio)

        form_layout.addLayout(radio_layout)

        # Spacer to separate radio buttons and instruction label
        spacer_1 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(spacer_1)

        # Instruction label
        create_product_entry_form.instruction_label = QLabel("Select from the above options to make an insertion")
        create_product_entry_form.instruction_label.setFont(QFont("Arial", 12))  # Reduced font size
        create_product_entry_form.instruction_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(create_product_entry_form.instruction_label)

        # Spacer to add space below the instruction label
        spacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(spacer_2)

        # Dynamic input fields section
        input_layout = QVBoxLayout()
        create_product_entry_form.fields = [
            ("Product ID:", create_product_entry_form.create_input_field()),
            ("Product Name:", create_product_entry_form.create_input_field()),
            ("Type:", create_product_entry_form.create_dropdown_from_db("SELECT Type_Name FROM tbl_Type")),
            ("Category:", create_product_entry_form.create_dropdown_from_db("SELECT Category_Name FROM tbl_Category")),
            ("Subcategory:", create_product_entry_form.create_dropdown_from_db("SELECT Sub_Category_Name FROM tbl_Sub_Category",True)),
            ("Quantity:", create_product_entry_form.create_input_field()),
            ("Price:",create_product_entry_form.create_input_field()),
            ("Shelf Life (Months):", create_product_entry_form.create_input_field()),
            ("Subcategory Name:", create_product_entry_form.create_input_field()),
            ("Category:", create_product_entry_form.create_dropdown_from_db("SELECT Category_Name FROM tbl_Category")),
            ("Type:", create_product_entry_form.create_dropdown_from_db("SELECT Type_Name FROM tbl_Type")),
            ("Category Name:", create_product_entry_form.create_input_field()),
            ("Type:", create_product_entry_form.create_dropdown_from_db("SELECT Type_Name FROM tbl_Type")),
            ("Type Name:", create_product_entry_form.create_input_field()),
        ]

        # Create placeholders for all fields
        create_product_entry_form.input_widgets = []
        for label, widget in create_product_entry_form.fields:
            row_layout = QHBoxLayout()
            label_widget = QLabel(label)
            label_widget.setFont(QFont("Arial", 14))
            widget.setFont(QFont("Arial", 14))
            label_widget.setVisible(False)
            widget.setVisible(False)
            row_layout.addWidget(label_widget)
            row_layout.addWidget(widget)
            input_layout.addLayout(row_layout)
            create_product_entry_form.input_widgets.append((label_widget, widget))

        form_layout.addLayout(input_layout)

        # Spacer to ensure consistent spacing below
        spacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(spacer_3)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.setFont(QFont("Arial", 14, QFont.Bold))
        submit_button.setStyleSheet("background-color: #4caf50; color: white;")
        submit_button.clicked.connect(create_product_entry_form.handle_submission)
        form_layout.addWidget(submit_button)

        # Set default selection for "Product"
        create_product_entry_form.product_radio.setChecked(True)
        create_product_entry_form.toggle_input_fields()

        # Connect radio button clicks to toggle fields
        create_product_entry_form.product_radio.clicked.connect(create_product_entry_form.toggle_input_fields)
        create_product_entry_form.category_radio.clicked.connect(create_product_entry_form.toggle_input_fields)
        create_product_entry_form.subcategory_radio.clicked.connect(create_product_entry_form.toggle_input_fields)
        create_product_entry_form.type_radio.clicked.connect(create_product_entry_form.toggle_input_fields)

        return form_frame

    @staticmethod
    def create_input_field():
        """Create an input field."""
        return QLineEdit()
    @staticmethod
    def create_dropdown_from_db( query, include_none_option=False):
        """Create a dropdown populated from the database."""
        combo_box = QComboBox()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                combo_box.addItem(row[0])
            if include_none_option:
                combo_box.insertItem(0, "None")
        except pyodbc.Error as e:
            create_product_entry_form.show_alert(f"An error occurred while loading dropdown: {str(e)}")
        return combo_box
    @staticmethod
    def toggle_input_fields():
        """Toggle visibility of input fields based on radio button selection."""
        #selected_button = create_product_entry_form.sender(QWidget)

        # Hide all fields initially
        for label_widget, widget in create_product_entry_form.input_widgets:
            label_widget.setVisible(False)
            widget.setVisible(False)

        # Show fields based on selected radio button
        if create_product_entry_form.product_radio.isChecked():
            for i in range(1, 8):  # Show product-related fields
                label_widget, widget = create_product_entry_form.input_widgets[i]
                label_widget.setVisible(True)
                widget.setVisible(True)

        elif create_product_entry_form.category_radio.isChecked():
            for i in range(11, 13):  # Show category-related fields
                label_widget, widget = create_product_entry_form.input_widgets[i]
                label_widget.setVisible(True)
                widget.setVisible(True)

        elif create_product_entry_form.subcategory_radio.isChecked():
            for i in range(8, 10):  # Show subcategory-related fields
                label_widget, widget = create_product_entry_form.input_widgets[i]
                label_widget.setVisible(True)
                widget.setVisible(True)

        elif create_product_entry_form.type_radio.isChecked():
            for i in range(13, 14):  # Show type-related fields
                label_widget, widget = create_product_entry_form.input_widgets[i]
                label_widget.setVisible(True)
                widget.setVisible(True)

    def handle_submission():
        """Handle form submission."""
        # Extract form values
        product_data = []

        if create_product_entry_form.product_radio.isChecked():
            # Iterate over widgets for product-related fields (indexes 1 to 7)
            for label_widget, widget in create_product_entry_form.input_widgets[1:8]:  # Slicing the list to get relevant fields
                # Check if widget is a QLineEdit or QComboBox
                if isinstance(widget, QLineEdit):
                    product_data.append(widget.text())  # For text input fields
                elif isinstance(widget, QComboBox):
                    product_data.append(widget.currentText())  # For dropdowns

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

                    # Retrieve the next available Product_ID by getting the max value and adding 1
                    cursor.execute("SELECT MAX(Product_ID) FROM tbl_product")
                    result = cursor.fetchone()
                    new_product_id = result[0] + 1 if result[0] is not None else 1  # If no product exists, start from 1

                    # Call the stored procedure (Product_ID is now explicitly passed)
                    cursor.execute(
                        "EXEC InsertProductAndLinkSubcategory ?, ?, ?, ?, ?, ?, ?, ?",
                        (
                            new_product_id,         # @ProductID (generated automatically)
                            product_name,           # @ProductName
                            type_name,              # @TypeName
                            category_name,          # @CategoryName
                            subcategory_name,       # @SubCategoryName
                            quantity,               # @Quantity
                            price,                  # @Price
                            shelf_life              # @ShelfLife
                        )
                    )
                    # cnxn.commit()
                    # cursor.execute("EXEC trg_insert_pricehistory")  # Replace with actual trigger procedure name

                    cnxn.commit()

                    create_product_entry_form.show_alert("Product added successfully!")

                except pyodbc.Error as e:
                    # Handle specific SQL errors
                    if "50003" in str(e):  # Check for duplicate product error code
                        create_product_entry_form.show_alert("Product already exists in the database.")
                    else:
                        error_message = f"An error occurred while inserting product: {str(e)}"
                        print(error_message)  # Log the error in the console
                        create_product_entry_form.show_alert(error_message)  # Display error in the alert box

                except ValueError as e:
                    error_message = f"Validation error: {str(e)}"
                    print(error_message)  # Log the error in the console
                    create_product_entry_form.show_alert(error_message)  # Display error in the alert box

            else:
                create_product_entry_form.show_alert("Please fill out all the required fields.")

        elif create_product_entry_form.category_radio.isChecked():
            # Clear previous data
            product_data = []

            # Iterate over widgets for category-related fields (indexes 11 to 13)
            for label_widget, widget in create_product_entry_form.input_widgets[11:13]:  # Slicing the list to get relevant fields
                # Check if widget is a QLineEdit or QComboBox
                if isinstance(widget, QLineEdit):
                    product_data.append(widget.text().strip())  # Trim whitespace for text input fields
                elif isinstance(widget, QComboBox):
                    product_data.append(widget.currentText().strip())  # Trim whitespace for dropdowns

            # Ensure the data list is not empty and matches the required number of fields
            if len(product_data) == 2:  # Adjust this number if your fields change
                try:
                    # Retrieve the next available Category_ID by getting the max value and adding 1
                    cursor.execute("SELECT MAX(Category_ID) FROM tbl_category")
                    result = cursor.fetchone()
                    new_category_id = result[0] + 1 if result[0] is not None else 1  # If no category exists, start from 1

                    category_name = product_data[0]
                    type_name = product_data[1]

                    # Validate user inputs
                    if not category_name or not type_name:
                        raise ValueError("Both Category Name and Type Name are required.")

                    # Call the stored procedure
                    cursor.execute(
                        "EXEC InsertCategory ?, ?, ?",
                        (
                            new_category_id,             # New Category_ID (generated automatically)
                            category_name,               # @CategoryName
                            type_name                    # @TypeName
                        )
                    )
                    cnxn.commit()
                    create_product_entry_form.show_alert("Category added successfully!")

                except pyodbc.Error as e:
                    # Handle exception for duplicate category
                    error_message = f"An error occurred while inserting category: {str(e)}"
                    print(error_message)  # Log the error in the console
                    create_product_entry_form.show_alert(error_message)  # Display error in the alert box

                except ValueError as e:
                    error_message = f"Validation error: {str(e)}"
                    print(error_message)  # Log the error in the console
                    create_product_entry_form.show_alert(error_message)  # Display error in the alert box

                else:
                    create_product_entry_form.show_alert("Please fill out all the required fields.")

        elif create_product_entry_form.type_radio.isChecked():
            # Clear previous data
            product_data = []

            # Iterate over widgets for type-related fields (indexes 13 to 14)
            for label_widget, widget in create_product_entry_form.input_widgets[13:14]:  # Slicing the list to get relevant fields
                # Check if widget is a QLineEdit or QComboBox
                if isinstance(widget, QLineEdit):
                    product_data.append(widget.text().strip())  # Trim whitespace for text input fields
                elif isinstance(widget, QComboBox):
                    product_data.append(widget.currentText().strip())  # Trim whitespace for dropdowns

            # Ensure the data list is not empty and matches the required number of fields
            if len(product_data) == 1:  # Adjust this number if your fields change
                try:
                    # Retrieve the next available Type_ID by getting the max value and adding 1
                    cursor.execute("SELECT MAX(Type_ID) FROM tbl_type")
                    result = cursor.fetchone()
                    new_type_id = result[0] + 1 if result[0] is not None else 1  # If no type exists, start from 1

                    type_name = product_data[0]

                    # Validate user input
                    if not type_name:
                        raise ValueError("Type Name is required.")

                    # Call the stored procedure
                    cursor.execute(
                        "EXEC InsertType ?, ?",
                        (
                            new_type_id,               # New Type_ID (generated automatically)
                            type_name                  # @TypeName
                        )
                    )
                    cnxn.commit()
                    create_product_entry_form.show_alert("Type added successfully!")

                except pyodbc.Error as e:
                    # Handle exception for duplicate type
                    error_message = f"An error occurred while inserting type: {str(e)}"
                    print(error_message)  # Log the error in the console
                    create_product_entry_form.show_alert(error_message)  # Display error in the alert box

                except ValueError as e:
                    error_message = f"Validation error: {str(e)}"
                    print(error_message)  # Log the error in the console
                    create_product_entry_form.show_alert(error_message)  # Display error in the alert box

            else:
                create_product_entry_form.show_alert("Please fill out the required field.")
        elif create_product_entry_form.subcategory_radio.isChecked():
            # Clear previous data
            product_data = []

            # Iterate over widgets for subcategory-related fields (indexes 8 to 10)
            for label_widget, widget in create_product_entry_form.input_widgets[8:10]:  # Slicing the list to get relevant fields
                # Check if widget is a QLineEdit or QComboBox
                if isinstance(widget, QLineEdit):
                    product_data.append(widget.text().strip())  # Trim whitespace for text input fields
                elif isinstance(widget, QComboBox):
                    product_data.append(widget.currentText().strip())  # Trim whitespace for dropdowns

            # Ensure the data list is not empty and matches the required number of fields
            if len(product_data) == 2:  # Adjust this number if your fields change
                try:
                    # Retrieve the next available SubCategory_ID by getting the max value and adding 1
                    cursor.execute("SELECT MAX(Sub_Category_ID) FROM tbl_Sub_Category")
                    result = cursor.fetchone()
                    new_subcategory_id = result[0] + 1 if result[0] is not None else 1  # If no subcategory exists, start from 1

                    subcategory_name = product_data[0]
                    category_name = product_data[1]

                    # Validate user inputs
                    if not subcategory_name or not category_name:
                        raise ValueError("Both Sub Category Name and Category Name are required.")

                    # Call the stored procedure
                    cursor.execute(
                        "EXEC InsertSubCategory ?, ?, ?",
                        (
                            new_subcategory_id,           # New SubCategory_ID (generated automatically)
                            subcategory_name,             # @SubcategoryName
                            category_name                 # @CategoryName
                        )
                    )
                    cnxn.commit()
                    create_product_entry_form.show_alert("SubCategory added successfully!")

                except pyodbc.Error as e:
                    # Handle exception for duplicate subcategory
                    error_message = f"An error occurred while inserting subcategory: {str(e)}"
                    print(error_message)  # Log the error in the console
                    create_product_entry_form.show_alert(error_message)  # Display error in the alert box

                except ValueError as e:
                    error_message = f"Validation error: {str(e)}"
                    print(error_message)  # Log the error in the console
                    create_product_entry_form.show_alert(error_message)  # Display error in the alert box

            else:
                create_product_entry_form.show_alert("Please fill out all the required fields.")

    @staticmethod  
    def show_alert(message):  
        #Show an alert message box 
        msg_box = QMessageBox()  
        msg_box.setIcon(QMessageBox.Information)  
        msg_box.setText(message)  
        msg_box.setWindowTitle("Information")  
        msg_box.exec_()

