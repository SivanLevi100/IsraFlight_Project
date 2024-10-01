from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateTimeEdit, QDoubleSpinBox,
    QPushButton, QComboBox, QMessageBox, QFormLayout, QWidget, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QSize
from models.Flight_model import Flight
from controllers.flight_controller import FlightController
from models.IsraelFlight_model import israel_flight_instance
from datetime import datetime

# Main dialog class for editing an existing flight
class EditFlightDialog(QDialog):
    def __init__(self, flight, admin_screen):
        super().__init__()

        self.flight = flight
        self.admin_screen = admin_screen
        self.setWindowTitle(f"Edit Flight - {flight.FlightId}")
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)

        self.setup_ui()

    # Set up the user interface for the dialog
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Title area
        title_frame = QFrame(self)
        title_frame.setStyleSheet(f"background-color: #0047AB;")

        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(40, 30, 40, 30)

        title_label = QLabel(f"Edit Flight")
        title_label.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: white; font-family: 'Segoe UI', Arial, sans-serif;"
        )

        flight_icon = QLabel()
        flight_icon.setPixmap(
            QIcon("IsraelFlight_Fronted_6419_6037/Images/edit_icon.png").pixmap(50, 50)
        )

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(flight_icon)

        main_layout.addWidget(title_frame)

        # Subtitle
        subtitle_label = QLabel(f"Flight ID: {self.flight.FlightId}")
        subtitle_label.setStyleSheet(
            "font-size: 18px; color: #0047AB; font-family: 'Segoe UI', Arial, sans-serif; margin-left: 40px;"
        )
        main_layout.addWidget(subtitle_label)

        # Form layout
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(40, 20, 40, 30)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form_layout.setHorizontalSpacing(40)  # Adds space between labels and fields

        
        self.add_form_field(form_layout, "Plane ID:", "PlaneId", field_type="combobox")
        self.add_form_field(form_layout, "Departure Location:", "DepartureLocation", field_type="combobox")
        self.add_form_field(form_layout, "Landing Location:", "LandingLocation", field_type="combobox")
        self.add_form_field(form_layout, "Departure Date Time:", "DepartureDateTime", field_type="datetime")
        self.add_form_field(form_layout, "Landing Date Time:", "EstimatedLandingDateTime", field_type="datetime")
        self.add_form_field(form_layout, "Flight Price:", "FlightPrice", field_type="doublespinbox")

        main_layout.addWidget(form_widget)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(40, 0, 40, 40)

        save_button = self.create_button(
            " Save",
            "#0047AB",
            "#FFFFFF",
            "IsraelFlight_Fronted_6419_6037/Images/save_icon.png",
        )
        save_button.clicked.connect(self.on_save_flight)

        cancel_button = self.create_button(
            " Cancel",
            "#0047AB",
            "#FFFFFF",
            "IsraelFlight_Fronted_6419_6037/Images/cancel_icon.png",
        )
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(button_layout)

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
                padding: 10px;
                border: 2px solid #0047AB;
                border-radius: 6px;
                background-color: white;
                font-size: 16px;
                min-width: 290px;
                max-width: 290px;
                color: #333333;
            }
            QLineEdit:focus, QDateTimeEdit:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 2px solid #4169E1;
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

    # Add a form field to the layout based on the field type
    def add_form_field(self, layout, label_text, field_name, field_type="lineedit"):
        label = QLabel(label_text)
        label.setMinimumWidth(160)  # Set a minimum width for labels to align them

        if field_type == "readonly":
            field = QLineEdit()
            field.setText(str(getattr(self.flight, field_name)))
            field.setReadOnly(True)
        elif field_type == "combobox":
            field = QComboBox()
            if field_name == "PlaneId":
                field.addItems([str(plane1.planeId) for plane1 in israel_flight_instance.planes])
                field.setCurrentText(str(self.flight.PlaneId))
            elif field_name in ["DepartureLocation", "LandingLocation"]:
                field.addItems([airport.iata for airport in israel_flight_instance.Airports])
                field.setCurrentText(getattr(self.flight, field_name))
        elif field_type == "datetime":
            field = QDateTimeEdit()
            field.setDateTime(getattr(self.flight, field_name))
            field.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        elif field_type == "doublespinbox":
            field = QDoubleSpinBox()
            field.setRange(0, 10000)
            field.setValue(self.flight.FlightPrice)
            field.setPrefix("$")
            field.setDecimals(2)
        else:
            field = QLineEdit()
            field.setText(str(getattr(self.flight, field_name)))

        layout.addRow(label, field)
        setattr(self, f"{field_name}_input", field)

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
                background-color: #003C91;
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

    # Handle the save flight action
    def on_save_flight(self):
        updated_flight = Flight(
            FlightId= self.flight.FlightId,
            PlaneId=int(self.PlaneId_input.currentText()),
            DepartureLocation=self.DepartureLocation_input.currentText(),
            LandingLocation=self.LandingLocation_input.currentText(),
            DepartureDateTime=self.DepartureDateTime_input.dateTime().toPython(),
            EstimatedLandingDateTime=self.EstimatedLandingDateTime_input.dateTime().toPython(),
            FlightPrice=self.FlightPrice_input.value()
        )
        FlightController.update_flight(updated_flight.FlightId, updated_flight.to_json())
        israel_flight_instance.Flights = [Flight.from_json(flight_data) for flight_data in FlightController.get_flights()]
        self.admin_screen.populate_flight_table(israel_flight_instance.Flights)
        self.show_success_message()
        self.accept()

    # Display a success message after updating a flight
    def show_success_message(self):
        success_box = QMessageBox(self)
        success_box.setIcon(QMessageBox.Information)
        success_box.setText("Flight details updated successfully!")
        success_box.setWindowTitle("Success")
        success_box.setStandardButtons(QMessageBox.Ok)

        ok_button = success_box.button(QMessageBox.Ok)
        ok_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0047AB;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #003C91;
            }
        """
        )
        success_box.exec()