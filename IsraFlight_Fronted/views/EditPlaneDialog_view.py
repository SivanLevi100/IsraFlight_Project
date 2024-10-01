from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton,
    QMessageBox, QFormLayout, QWidget, QFrame, QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QSize
from models.Plane_model import Plane
from controllers.plane_controller import PlaneController
from models.IsraelFlight_model import israel_flight_instance
from controllers.services_controller import ServicesController

# Main dialog class for editing an existing plane
class EditPlaneDialog(QDialog):
    def __init__(self, plane, admin_screen):
        super().__init__()

        self.plane = plane
        self.admin_screen = admin_screen
        self.setWindowTitle(f"Edit Plane - {plane.manufacturer} {plane.model}")
        self.setFixedSize(550, 700)
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

        title_label = QLabel(f"Edit Plane")
        title_label.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: white; font-family: 'Segoe UI', Arial, sans-serif;"
        )

        plane_icon = QLabel()
        plane_icon.setPixmap(
            QIcon("IsraelFlight_Fronted_6419_6037\Images\edit_icon.png").pixmap(50, 50)
        )

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(plane_icon)

        main_layout.addWidget(title_frame)

        # Subtitle
        subtitle_label = QLabel(f"Plane ID: {self.plane.planeId}")
        subtitle_label.setStyleSheet(
            "font-size: 18px; color: #0047AB; font-family: 'Segoe UI', Arial, sans-serif; margin-left: 40px;"
        )
        main_layout.addWidget(subtitle_label)

        # Form layout
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(40, 20, 40, 30)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.add_form_field(form_layout, "Manufacturer:", "manufacturer")
        self.add_form_field(form_layout, "Model:", "model")
        self.add_form_field(form_layout, "Year:", "year", field_type="spinbox")
        self.add_form_field(form_layout, "Nickname:", "nickname")
        self.add_form_field(form_layout, "Image URL:", "imageUrl")

        main_layout.addWidget(form_widget)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(40, 0, 40, 40)

        save_button = self.create_button(
            " Save",
            "#0047AB",
            "#FFFFFF",
            "IsraelFlight_Fronted_6419_6037\Images\save_icon.png",
        )
        save_button.clicked.connect(self.on_save_plane)

        cancel_button = self.create_button(
            " Cancel",
            "#0047AB",
            "#FFFFFF",
            "IsraelFlight_Fronted_6419_6037\Images\cancel_icon.png",
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
            QLineEdit, QSpinBox {
                padding: 12px;
                border: 2px solid #0047AB;
                border-radius: 6px;
                background-color: white;
                font-size: 16px;
                min-width: 250px;
                color: #333333;
            }
            QLineEdit:focus, QSpinBox:focus {
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

        if field_type == "spinbox":
            field = QSpinBox()
            field.setRange(1900, 2024)
            field.setValue(getattr(self.plane, "yearOfManufacture", 2000))
        else:
            field = QLineEdit()
            field.setText(getattr(self.plane, field_name, ""))

        layout.addRow(label, field)
        setattr(self, f"{field_name}_input", field)

    # Create a styled button with icon
    def create_button(self, text, bg_color, text_color, icon_path):
        button = QPushButton(text)
        button.setStyleSheet(
            f"""
            background-color: {bg_color};
            color: {text_color};
            text-align: center;
        """
        )
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #0047AB;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #003C91;
            }
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

    # Handle the save plane action
    def on_save_plane(self):
        updated_plane = Plane(
            str(self.plane.planeId),
            self.manufacturer_input.text(),
            self.model_input.text(),
            self.year_input.value(),
            self.nickname_input.text(),
            self.imageUrl_input.text(),
        )
        if ServicesController.validate_image(updated_plane.imageUrl):
            PlaneController.update_plane(self.plane.planeId, updated_plane.to_json())
            israel_flight_instance.planes = [
                Plane.from_json(plane_data)
                for plane_data in PlaneController.get_planes()
            ]
            self.admin_screen.populate_plane_cards(israel_flight_instance.planes)
            self.show_success_message()
            self.accept()
        else:
            self.show_error_message(
                "Invalid Image URL",
                "The image URL is not represent a plane image. Please check and try again.",
            )

    # Display a success message after updating a plane
    def show_success_message(self):
        success_box = QMessageBox(self)
        success_box.setIcon(QMessageBox.Information)
        success_box.setText("Plane details updated successfully!")
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
                color: #0047AB;
                border: 2px solid #0047AB;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0047AB;
                color: white;
            }
        """
        )
        error_box.exec()
        self.imageUrl_input.setFocus()