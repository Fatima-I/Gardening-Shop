import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QRadioButton, QHBoxLayout,
    QComboBox, QMessageBox, QFrame, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pyodbc
import matplotlib.pyplot as plt

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

class StatisticsView(QFrame):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Header
        title = QLabel("STATISTICS")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Radio Buttons for Year, Month, and Range
        radio_layout = QHBoxLayout()

        self.year_radio = QRadioButton("Year")
        self.year_radio.setFont(QFont("Arial", 14))
        self.year_radio.setChecked(True)  # Default selection
        radio_layout.addWidget(self.year_radio)

        self.month_radio = QRadioButton("Month")
        self.month_radio.setFont(QFont("Arial", 14))
        radio_layout.addWidget(self.month_radio)

        self.range_radio = QRadioButton("Range")
        self.range_radio.setFont(QFont("Arial", 14))
        radio_layout.addWidget(self.range_radio)

        layout.addLayout(radio_layout)

        # Year input field and label (initially visible)
        self.year_label = QLabel("Enter Year:")
        self.year_label.setFont(QFont("Arial", 14))
        self.year_input = QLineEdit()
        self.year_input.setFont(QFont("Arial", 14))
        self.year_input.setPlaceholderText("YYYY")  # Default text for Year (YYYY)

        # Month input field and label (initially hidden)
        self.month_label = QLabel("Enter Month:")
        self.month_label.setFont(QFont("Arial", 14))
        self.month_input = QLineEdit()
        self.month_input.setFont(QFont("Arial", 14))
        self.month_input.setPlaceholderText("MM")  # Default text for Month (MM)

        # Min and Max input fields and labels for Range (initially hidden)
        self.min_label = QLabel("Enter Min Value:")
        self.min_label.setFont(QFont("Arial", 14))
        self.min_input = QLineEdit()
        self.min_input.setFont(QFont("Arial", 14))
        self.min_input.setPlaceholderText("YYYY-MM-DD") # Default text for Min

        self.max_label = QLabel("Enter Max Value:")
        self.max_label.setFont(QFont("Arial", 14))
        self.max_input = QLineEdit()
        self.max_input.setFont(QFont("Arial", 14))
        self.max_input.setPlaceholderText("YYYY-MM-DD")  # Default text for Min

        layout.addWidget(self.year_label)
        layout.addWidget(self.year_input)

        # Initially, the month and range input fields should be hidden
        layout.addWidget(self.month_label)
        layout.addWidget(self.month_input)
        layout.addWidget(self.min_label)
        layout.addWidget(self.min_input)
        layout.addWidget(self.max_label)
        layout.addWidget(self.max_input)

        self.month_label.setVisible(False)
        self.month_input.setVisible(False)
        self.min_label.setVisible(False)
        self.min_input.setVisible(False)
        self.max_label.setVisible(False)
        self.max_input.setVisible(False)

        # Placeholder for statistics data (e.g., a table or chart)
        self.statistics_data = QLabel("Statistics data will appear here.")
        self.statistics_data.setFont(QFont("Arial", 12))
        self.statistics_data.setAlignment(Qt.AlignCenter)
        self.statistics_data.setStyleSheet("color: gray;")
        layout.addWidget(self.statistics_data)

        # Table for showing the statistics (name, total purchase, total sale, profit)
        self.statistics_table = QTableWidget()
        self.statistics_table.setColumnCount(4)
        self.statistics_table.setHorizontalHeaderLabels(["Name", "Total Purchase", "Total Sale", "Profit"])
        self.statistics_table.setVisible(True)  # Initially visible for testing
        layout.addWidget(self.statistics_table)

        # Submit Button to show statistics
        submit_button = QPushButton("Show Statistics")
        submit_button.setFont(QFont("Arial", 14, QFont.Bold))
        submit_button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        submit_button.clicked.connect(self.show_statistics)
        layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        layout.addStretch()

        # Connect radio buttons to toggle visibility of inputs
        self.year_radio.toggled.connect(self.toggle_inputs)
        self.month_radio.toggled.connect(self.toggle_inputs)
        self.range_radio.toggled.connect(self.toggle_inputs)

    def toggle_inputs(self):
        """Toggle visibility of year, month, and range input fields based on selected radio button."""
        if self.year_radio.isChecked():
            self.year_label.setVisible(True)
            self.year_input.setVisible(True)
            self.month_label.setVisible(False)
            self.month_input.setVisible(False)
            self.min_label.setVisible(False)
            self.min_input.setVisible(False)
            self.max_label.setVisible(False)
            self.max_input.setVisible(False)
        elif self.month_radio.isChecked():
            self.year_label.setVisible(True)
            self.year_input.setVisible(True)
            self.month_label.setVisible(True)
            self.month_input.setVisible(True)
            self.min_label.setVisible(False)
            self.min_input.setVisible(False)
            self.max_label.setVisible(False)
            self.max_input.setVisible(False)
        elif self.range_radio.isChecked():
            self.year_label.setVisible(False)
            self.year_input.setVisible(False)
            self.month_label.setVisible(False)
            self.month_input.setVisible(False)
            self.min_label.setVisible(True)
            self.min_input.setVisible(True)
            self.max_label.setVisible(True)
            self.max_input.setVisible(True)

    def show_statistics(self):
        """Handle displaying statistics based on selected option."""
        year = self.year_input.text()
        month = self.month_input.text()
        min_value = self.min_input.text()
        max_value = self.max_input.text()

        if self.year_radio.isChecked():
            if year:
                self.statistics_data.setText(f"Displaying statistics for the year {year}...")
                self.generate_graph(year)
                self.populate_statistics_table(year, month=None, min_value=None, max_value=None)
            else:
                self.statistics_data.setText("Please enter a valid year.")
        elif self.month_radio.isChecked():
            if year and month:
                self.statistics_data.setText(f"Displaying statistics for {month} {year}...")
                self.generate_graph(year, month)
                self.populate_statistics_table(year, month, min_value=None, max_value=None)
            else:
                self.statistics_data.setText("Please enter both year and month.")
        elif self.range_radio.isChecked():
            if year and min_value and max_value:
                self.statistics_data.setText(f"Displaying statistics for the range {min_value} - {max_value} in {year}...")
                self.generate_graph(year, month=None, range_min=min_value, range_max=max_value)
                self.populate_statistics_table(year, month=None, min_value=min_value, max_value=max_value)
            else:
                self.statistics_data.setText("Please enter year, min, and max values.")


    def generate_graph(self, year, month=None, range_min=None, range_max=None):
        """Generate a graph based on the statistics for the year, month, or range."""
        cnxn, cursor = get_db_connection()

        try:
            if month:
                # Call stored procedure for Year + Month
                cursor.execute("EXEC GetGraphData @Year = ?, @Month = ?", (year, month))
            elif range_min and range_max:
                # Call stored procedure for Date Range
                cursor.execute("EXEC GetGraphData @Year = ?, @MinDate = ?, @MaxDate = ?", (year, range_min, range_max))
            else:
                # Default case for Year only
                cursor.execute("EXEC GetGraphData @Year = ?", (year,))

            result = cursor.fetchall()

            # Prepare data for the graph
            periods = []
            purchase_data = []
            sale_data = []

            for row in result:
                periods.append(row[0])  # Period (Month/Day)
                purchase_data.append(row[1])  # Total Purchase Amount
                sale_data.append(row[2])  # Total Sale Amount

            
            print(periods)
            print(purchase_data)
            print(sale_data)

            # Sort the periods to ensure months are ordered correctly
            sorted_data = sorted(zip(periods, purchase_data, sale_data), key=lambda x: self.get_month_number(x[0]))
            periods, purchase_data, sale_data = zip(*sorted_data)

            # Create the graph
            plt.figure(figsize=(10, 6))
            bar_width = 0.35
            index = range(len(periods))

            # Create bars for purchases and sales
            plt.bar(index, purchase_data, bar_width, label="Total Purchase", color='blue', alpha=0.6)
            plt.bar([i + bar_width for i in index], sale_data, bar_width, label="Total Sale", color='green', alpha=0.6)

            plt.title(f"Sales and Purchases for {year}" + (f" - {month}" if month else ""))
            plt.xlabel("Period")
            plt.ylabel("Amount")
            plt.xticks([i + bar_width / 2 for i in index], periods, rotation=45, ha='right')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while generating the graph: {str(e)}")

        finally:
            cursor.close()
            cnxn.close()

    def get_month_number(self, month_name):
        """Helper function to convert month name to month number."""
        months = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        return months.get(month_name, 0)


    def populate_statistics_table(self, year, month=None, min_value=None, max_value=None):
        """Populate the table with statistics data (name, total purchase, total sale, profit)."""
        cnxn, cursor = get_db_connection()

        try:
            if month:
                # Call stored procedure for Year + Month
                cursor.execute("EXEC GetStatisticsData @Year = ?, @Month = ?", (year, month))
            elif min_value and max_value:
                # Call stored procedure for Date Range
                cursor.execute("EXEC GetStatisticsData @Year = ?, @MinDate = ?, @MaxDate = ?", (year, min_value, max_value))
            else:
                # Default case for Year only
                cursor.execute("EXEC GetStatisticsData @Year = ?", (year,))

            result = cursor.fetchall()

            # Clear previous table entries
            self.statistics_table.setRowCount(0)

            # Insert the fetched data into the table
            for row_index, row in enumerate(result):
                # Assuming row structure: (Product_Name, Total_Purchase_Amount, Total_Sale_Amount, Profit)
                self.statistics_table.insertRow(row_index)
                self.statistics_table.setItem(row_index, 0, QTableWidgetItem(row[0]))  # Product Name
                self.statistics_table.setItem(row_index, 1, QTableWidgetItem(str(row[1])))  # Total Purchase Amount
                self.statistics_table.setItem(row_index, 2, QTableWidgetItem(str(row[2])))  # Total Sale Amount
                self.statistics_table.setItem(row_index, 3, QTableWidgetItem(str(row[3])))  # Profit

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while fetching statistics: {str(e)}")

        finally:
            # Close database connection
            cursor.close()
            cnxn.close()


