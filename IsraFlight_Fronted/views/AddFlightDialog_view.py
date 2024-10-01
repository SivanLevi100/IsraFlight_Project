from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateTimeEdit, QDoubleSpinBox,
    QPushButton, QComboBox, QMessageBox, QFormLayout, QWidget, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QSize, QDateTime
from models.Flight_model import Flight
from controllers.flight_controller import FlightController
from models.IsraelFlight_model import israel_flight_instance

# Main dialog class for adding a new flight
class FlightDialog(QDialog):
    def __init__(self, admin_screen):
        super().__init__()

        self.admin_screen = admin_screen
        self.setWindowTitle("Add New Flight")
        self.setFixedSize(550, 750)
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)

        self.setup_ui()

    # Set up the user interface for the dialog
    def setup_ui(self):
        # Main layout setup
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Title area
        title_frame = QFrame(self)
        title_frame.setStyleSheet(f"background-color: #4a90e2;")

        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(40, 30, 40, 30)

        title_label = QLabel("Add New Flight")
        title_label.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: white; font-family: 'Segoe UI', Arial, sans-serif;"
        )

        flight_icon = QLabel()
        flight_icon.setPixmap(
            QIcon("IsraelFlight_Fronted_6419_6037\Images\Flight_icon.png").pixmap(80, 80)
        )

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(flight_icon)

        main_layout.addWidget(title_frame)

        # Subtitle (Flight ID)
        self.flight_id = israel_flight_instance.Flights[-1].FlightId + 1
        subtitle_label = QLabel(f"Flight ID: {self.flight_id}")
        subtitle_label.setStyleSheet(
            "font-size: 18px; color: #4a90e2; font-family: 'Segoe UI', Arial, sans-serif; margin-left: 40px;"
        )
        main_layout.addWidget(subtitle_label)

        # Form layout
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(40, 20, 40, 30)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        # Input fields
        self.plane_id_input = QComboBox()
        self.plane_id_input.addItems([str(plane1.planeId) for plane1 in israel_flight_instance.planes])
        self.add_input_field(form_layout, "Plane ID:", self.plane_id_input)

        self.departure_location_input = QComboBox()
        self.departure_location_input.addItems([airport.iata for airport in israel_flight_instance.Airports])
        self.add_input_field(form_layout, "Departure Location:", self.departure_location_input)

        self.landing_location_input = QComboBox()
        self.landing_location_input.addItems([airport.iata for airport in israel_flight_instance.Airports])
        self.add_input_field(form_layout, "Landing Location:", self.landing_location_input)

        self.departure_datetime_input = QDateTimeEdit()
        self.departure_datetime_input.setCalendarPopup(True)
        self.departure_datetime_input.setDateTime(QDateTime.currentDateTime())
        self.add_input_field(form_layout, "Departure Date Time:", self.departure_datetime_input)

        self.estimated_landing_datetime_input = QDateTimeEdit()
        self.estimated_landing_datetime_input.setCalendarPopup(True)
        self.estimated_landing_datetime_input.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.add_input_field(form_layout, "Landing Date Time:", self.estimated_landing_datetime_input)

        self.flight_price_input = QDoubleSpinBox()
        self.flight_price_input.setRange(0, 10000)
        self.flight_price_input.setDecimals(2)
        self.add_input_field(form_layout, "Flight Price:", self.flight_price_input)

        main_layout.addWidget(form_widget)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(40, 0, 40, 40)

        add_button = self.create_button(
            " Add",
            "#4a90e2",
            "#FFFFFF",
            "IsraelFlight_Fronted_6419_6037/Images/plus_icon.png",
        )
        add_button.clicked.connect(self.on_add_flight)

        cancel_button = self.create_button(
            " Cancel",
            "#4a90e2",
            "#FFFFFF",
            "IsraelFlight_Fronted_6419_6037/Images/cancel_icon.png",
        )
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(button_layout)

        # Set stylesheet
        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #333333;
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit, QDateTimeEdit, QDoubleSpinBox, QComboBox {
                padding: 12px;
                border: 2px solid #4a90e2;
                border-radius: 6px;
                background-color: white;
                font-size: 16px;
                min-width: 250px;
                color: #333333;
            }
            QLineEdit:focus, QDateTimeEdit:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 2px solid #3a7bc8;
            }
            QPushButton {
                border: none;
                border-radius: 18px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
        """
        )

    # Helper method to add a label and input field to the dialog layout
    def add_input_field(self, layout, label_text, input_widget):
        label = QLabel(label_text)
        layout.addRow(label, input_widget)

    # Create a styled button with icon
    def create_button(self, text, bg_color, text_color, icon_path):
        button = QPushButton(text)
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 16px;
            }}
            QPushButton:hover {{
                background-color: #3a7bc8;
            }}
        """
        )

        icon = QIcon(icon_path)
        button.setIcon(icon)
        button.setIconSize(QSize(24, 24))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 3)
        button.setGraphicsEffect(shadow)

        return button

    # Handle the add flight action
    def on_add_flight(self):
        # Create new flight and add it to the database
        new_flight = self.get_flight()
        FlightController.add_flight(new_flight.to_json())
        print(new_flight.to_json())
        israel_flight_instance.Flights = [
            Flight.from_json(flight_data)
            for flight_data in FlightController.get_flights()
        ]
        self.admin_screen.populate_flight_table(israel_flight_instance.Flights)
        self.show_success_message()
        self.accept()
        self.hide()

    # Create and return a Flight object from input fields
    def get_flight(self):
        return Flight(
            self.flight_id,
            self.plane_id_input.currentText(),
            self.departure_location_input.currentText(),
            self.landing_location_input.currentText(),
            self.departure_datetime_input.dateTime().toPython(),
            self.estimated_landing_datetime_input.dateTime().toPython(),
            self.flight_price_input.value(),
        )

    # Display a success message after adding a flight
    def show_success_message(self):
        # Show success message box
        success_box = QMessageBox(self)
        success_box.setIcon(QMessageBox.Information)
        success_box.setText("New flight added successfully!")
        success_box.setWindowTitle("Success")
        success_box.setStandardButtons(QMessageBox.Ok)

        ok_button = success_box.button(QMessageBox.Ok)
        ok_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3a7bc8;
            }
        """
        )
        success_box.exec()