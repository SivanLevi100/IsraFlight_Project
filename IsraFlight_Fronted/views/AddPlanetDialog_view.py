from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton,
    QMessageBox, QFormLayout, QWidget, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QSize
from models.Plane_model import Plane
from controllers.plane_controller import PlaneController
from models.IsraelFlight_model import israel_flight_instance
from controllers.services_controller import ServicesController

# Main dialog class for adding a new plane
class PlaneDialog(QDialog):
    def __init__(self, admin_screen):
        super().__init__()

        self.admin_screen = admin_screen
        self.setWindowTitle("Add New Plane")
        self.setFixedSize(550, 650)
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)

        self.setup_ui()

    # Set up the user interface for the dialog
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Title area
        title_frame = QFrame(self)
        title_frame.setStyleSheet(f"background-color: #4a90e2;")

        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(40, 30, 40, 30)

        title_label = QLabel("Add New Plane")
        title_label.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: white; font-family: 'Segoe UI', Arial, sans-serif;"
        )

        plane_icon = QLabel()
        plane_icon.setPixmap(
            QIcon("IsraelFlight_Fronted_6419_6037/Images/plane_icon.png").pixmap(50, 50)
        )

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(plane_icon)

        main_layout.addWidget(title_frame)

        # Subtitle (Plane ID)
        self.plane_id = israel_flight_instance.planes[-1].planeId + 1
        subtitle_label = QLabel(f"Plane ID: {self.plane_id}")
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

        self.add_input_field(form_layout, "Manufacturer:", QLineEdit())
        self.add_input_field(form_layout, "Model:", QLineEdit())
        self.year_of_manufacture_input = QSpinBox()
        self.year_of_manufacture_input.setRange(1900, 2024)
        self.add_input_field(form_layout, "Year of Manufacture:", self.year_of_manufacture_input)
        self.add_input_field(form_layout, "Nickname:", QLineEdit())
        self.add_input_field(form_layout, "Image URL:", QLineEdit())

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
        add_button.clicked.connect(self.on_add_plane)

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
            QLineEdit, QSpinBox {
                padding: 12px;
                border: 2px solid #4a90e2;
                border-radius: 6px;
                background-color: white;
                font-size: 16px;
                min-width: 250px;
                color: #333333;
            }
            QLineEdit:focus, QSpinBox:focus {
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
        if isinstance(input_widget, QLineEdit):
            setattr(self, f"{label_text.lower().replace(' ', '_').replace(':', '')}_input", input_widget)

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

    # Handle the add plane action
    def on_add_plane(self):
        new_plane = self.get_plane()
        image_url = self.image_url_input.text()
        print(image_url)
        if ServicesController.validate_image(image_url):
            PlaneController.add_plane(new_plane.to_json())  # Calling POST method
            print(new_plane.to_json())
            israel_flight_instance.planes = [Plane.from_json(plane_data) for plane_data in PlaneController.get_planes()]
            self.admin_screen.populate_plane_cards(israel_flight_instance.planes)
            self.show_success_message()
            self.accept()
            self.hide()
        else:
            self.show_error_message("Error", "The image URL is not valid or does not represent a plane image.")
            self.image_url_input.clear()

    # Create and return a Plane object from input fields
    def get_plane(self):
        plane = Plane(
            str(self.plane_id),
            self.manufacturer_input.text(),
            self.model_input.text(),
            self.year_of_manufacture_input.value(),
            self.nickname_input.text(),
            self.image_url_input.text()
        )
        print(plane)
        return plane

    # Display a success message after adding a plane
    def show_success_message(self):
        success_box = QMessageBox(self)
        success_box.setIcon(QMessageBox.Information)
        success_box.setText("New plane added successfully!")
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

    # Display an error message for invalid input
    def show_error_message(self, title, message):
        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Warning)
        error_box.setText(message)
        error_box.setWindowTitle(title)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.button(QMessageBox.Ok).setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                color: #4a90e2;
                border: 2px solid #4a90e2;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4a90e2;
                color: white;
            }
        """
        )
        error_box.exec()
        self.image_url_input.setFocus()