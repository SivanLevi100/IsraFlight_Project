from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QDialog,
    QComboBox, QMessageBox, QListWidget
)
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from models.IsraelFlight_model import israel_flight_instance
from views.AddFlightDialog_view import FlightDialog
from views.EditFlightDialog_view import EditFlightDialog
from controllers.flight_controller import FlightController
from controllers.booking_Controller import BookingController
from models.Flight_model import Flight

# Main class for displaying and managing the list of flights
class FlightListScreen(QWidget):
    def __init__(self, home_screen):
        super().__init__()
        self.home_screen = home_screen
        self.setup_ui()
        self.populate_flight_table(israel_flight_instance.Flights)

    # Set up the user interface
    def setup_ui(self):
        self.setWindowIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\logo_icon.png"))
        self.setWindowTitle("Flights Management")
        self.setGeometry(100, 100, 1200, 800)
        self.showMaximized()
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F8FF;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #0047AB;
                color: white;
                border: none;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3a7bc8;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.create_top_bar())

        # Content area
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(30, 30, 30, 30)

        # Add Flight button and Filter combo box
        top_controls_layout = QHBoxLayout()
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Flights", "Departures", "Arrivals"])
        self.filter_combo.setStyleSheet("""
    QComboBox {
        background-color: white;
        border: 2px solid #4a90e2;
        border-radius: 5px;
        padding: 5px 25px 5px 10px;
        min-width: 130px;
        max-width: 130px;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
        font-weight: bold;
        color: #333;
    }
    QComboBox:hover {
        border-color: #2980b9;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left-width: 2px;
        border-left-color: #4a90e2;
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }
    QComboBox::down-arrow {
        image: url(IsraelFlight_Fronted_6419_6037/Images/dropdown_arrow.png);
        width: 12px;
        height: 12px;
    }
    QComboBox QAbstractItemView {
        border: 2px solid #4a90e2;
        selection-background-color: #e6f3ff;
        selection-color: #333;
    }
""")
        self.filter_combo.currentIndexChanged.connect(self.filter_flights)
        top_controls_layout.addWidget(self.filter_combo, alignment=Qt.AlignLeft)
        
        add_flight_button = QPushButton("  Add Flight")
        add_flight_button.setFont(QFont("Arial", 12))
        add_flight_button.setFixedSize(150, 40)
        add_flight_button.setIcon(QIcon("IsraelFlight_Fronted_6419_6037/Images/plus_icon.png"))
        add_flight_button.setIconSize(QSize(20, 20))
        add_flight_button.clicked.connect(self.add_flight)
        add_flight_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #28558B;
            }
            """
        )
        top_controls_layout.addWidget(add_flight_button)
        
        content_layout.addLayout(top_controls_layout)

        # Flights Table
        self.flight_table = QTableWidget()
        self.flight_table.setColumnCount(8)  # Added one more column for delete button
        self.flight_table.setHorizontalHeaderLabels([
            "Flight ID", "Plane ID", "Departure Location", "Landing Location",
            "Departure Date Time", "Landing Date Time", "Flight Price", "Delete"
        ])
        self.flight_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.flight_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.flight_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E0E0E0;
                alternate-background-color: #F0F8FF;
            }
            QHeaderView::section {
                background-color: #0047AB;
                color: white;
                padding: 5px;
                border: 1px solid white;
            }
        """)
        self.flight_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.flight_table.verticalHeader().setVisible(False)
        self.flight_table.setAlternatingRowColors(True)
        self.flight_table.itemDoubleClicked.connect(self.modify_flight)
        content_layout.addWidget(self.flight_table)

        main_layout.addLayout(content_layout)
        main_layout.addWidget(self.create_bottom_bar())

    # Create the top bar of the screen
    def create_top_bar(self):
        top_bar = QFrame()
        top_bar.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-bottom: 2px solid #2980B9;
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 10, 20, 10)

        logo_label = QLabel()
        logo_label.setPixmap(QIcon("IsraelFlight_Fronted_6419_6037\Images\IsraelFlight_logo.png").pixmap(QSize(150, 150)))
        logo_label.setStyleSheet("border: None;")
        top_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        title_label = QLabel("Flight Management")
        title_label.setStyleSheet("""
            font-size: 35px;
            font-weight: bold;
            color: #0047AB;
            border: None;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(title_label, 1)

        home_button = QPushButton()
        home_button.setIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\back_icon.png"))
        home_button.setIconSize(QSize(32, 32))
        home_button.setFixedSize(50, 50)
        home_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #2980B9;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #E6F2FF;
            }
        """)
        home_button.clicked.connect(self.go_to_home_screen)
        top_layout.addWidget(home_button, alignment=Qt.AlignRight)

        return top_bar

    # Create the bottom bar of the screen
    def create_bottom_bar(self):
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                border: none;
            }
        """)

        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(20, 10, 20, 10)

        footer_text = QLabel("Version 1.0.3   |   © 2024 Israel Flight   |   support@israelflight.com   |   Tel: +972-3-1234567   |   Terms of Service   |   Privacy Policy   ")
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setStyleSheet("""
            color: #FFFFFF;
            font-size: 13px;
            font-weight: bold;
        """)
        bottom_layout.addWidget(footer_text)

        return bottom_bar

    # Navigate back to the home screen
    def go_to_home_screen(self):
        self.home_screen.show()
        self.close()

    # Populate the flight table with data
    def populate_flight_table(self, flights):
        self.flight_table.setRowCount(len(flights))
        for row, flight in enumerate(flights):
            # Helper function to create centered items
            def create_centered_item(value):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                return item

            # Set table items
            self.flight_table.setItem(row, 0, create_centered_item(flight.FlightId))
            self.flight_table.setItem(row, 1, create_centered_item(flight.PlaneId))
            self.flight_table.setItem(row, 2, create_centered_item(flight.DepartureLocation))
            self.flight_table.setItem(row, 3, create_centered_item(flight.LandingLocation))
            self.flight_table.setItem(row, 4, create_centered_item(flight.DepartureDateTime.strftime('%Y-%m-%d %H:%M:%S')))
            self.flight_table.setItem(row, 5, create_centered_item(flight.EstimatedLandingDateTime.strftime('%Y-%m-%d %H:%M:%S')))
            self.flight_table.setItem(row, 6, create_centered_item(f"${flight.FlightPrice:.2f}"))

            # Create delete button
            delete_button = QPushButton()
            delete_button.setIcon(QIcon("IsraelFlight_Fronted_6419_6037/Images/trash_icon.png"))
            delete_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
                QPushButton:hover {
                    background-color: #E8F6FF;
                    border-radius: 20px;
                }
            """)
            delete_button.clicked.connect(lambda _, f_id=flight.FlightId: self.delete_flight(f_id))
            
            # Center the delete button in the cell
            button_container = QWidget()
            button_layout = QHBoxLayout(button_container)
            button_layout.addWidget(delete_button)
            button_layout.setAlignment(Qt.AlignCenter)
            button_layout.setContentsMargins(0, 0, 0, 0)
            
            self.flight_table.setCellWidget(row, 7, button_container)

    # Add a new flight
    def add_flight(self):
        dialog = FlightDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.populate_flight_table(israel_flight_instance.Flights)

    # Modify an existing flight
    def modify_flight(self, item):
        row = item.row()
        flight_id = int(self.flight_table.item(row, 0).text())
        flight = next((flight for flight in israel_flight_instance.Flights if flight.FlightId == flight_id), None)
        if flight:
            dialog = EditFlightDialog(flight, self)
            if dialog.exec() == QDialog.Accepted:
                self.populate_flight_table(israel_flight_instance.Flights)

    # Delete a flight
    def delete_flight(self, flight_id):
        # Create a confirmation dialog
        confirm_dialog = QMessageBox(self)
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setText(f"Are you sure you want to delete the flight with ID {flight_id}?")
        confirm_dialog.setWindowTitle("Confirm Deletion")
        confirm_dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm_dialog.setDefaultButton(QMessageBox.Cancel)

        # Show the dialog and get the result
        result = confirm_dialog.exec()
        confirm_dialog.hide()

        # If OK was pressed, check for associated bookings and then delete the flight
        if result == QMessageBox.Ok:
            try:
                # Check if the flight is associated with any bookings
                all_bookings = israel_flight_instance.Bookings
                if isinstance(all_bookings, str) and all_bookings.startswith("Error"):
                    raise Exception(f"Failed to retrieve bookings: {all_bookings}")

                associated_bookings = [
                    booking for booking in all_bookings
                    if booking.flightId == flight_id
                ]

                if associated_bookings:
                    # If there are associated bookings, show a warning and don't delete
                    booking_ids = ", ".join(
                        [str(booking.bookingId) for booking in associated_bookings]
                    )
                    QMessageBox.warning(
                        self,
                        "Cannot Delete",
                        f"This flight cannot be deleted because it is associated with the following bookings: {booking_ids}. Please remove these bookings first.",
                    )
                else:
                    # If no associated bookings, proceed with deletion
                    FlightController.delete_flight(flight_id)
                    
                    # Update the flights list
                    israel_flight_instance.Flights = [
                        Flight.from_json(flight_data) for flight_data in FlightController.get_flights()
                    ]

                    # Update the UI
                    self.populate_flight_table(israel_flight_instance.Flights)

                    # Show a success message
                    QMessageBox.information(
                        self, "Success", f"The flight with ID {flight_id} has been deleted successfully."
                    )
            except Exception as e:
            # For any error
              QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while deleting the flight: {str(e)}",
            )


    def filter_flights(self, index):
        filter_option = self.filter_combo.currentText()
        if filter_option == "All Flights":
            self.populate_flight_table(israel_flight_instance.Flights)
        elif filter_option == "Departures":
            filtered_flights = [f for f in israel_flight_instance.Flights if f.DepartureLocation == "TLV"]
            self.populate_flight_table(filtered_flights)
        elif filter_option == "Arrivals":
            filtered_flights = [f for f in israel_flight_instance.Flights if f.LandingLocation == "TLV"]
            self.populate_flight_table(filtered_flights)