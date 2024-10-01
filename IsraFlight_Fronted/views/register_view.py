from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDateEdit,
    QScrollArea,
    QFrame,
    QMessageBox,
    QDialog,
)
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QFont, QPixmap, QIcon
from models.FrequentFlyer_model import FrequentFlyer
from models.IsraelFlight_model import israel_flight_instance
from controllers.FrequentFlyer_Controller import FrequentFlyerController
from views.frequent_flyer_view import FrequentFlyerScreen


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register New User")
        self.setFixedSize(450, 620)
        self.setModal(True)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QWidget(self)
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #4A90E2;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # יצירת widget מרכזי לאייקון והתווית
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setSpacing(10)  # מרווח בין האייקון לתווית

        plane_icon = QLabel()
        plane_icon.setPixmap(
            QIcon(r"IsraelFlight_Fronted_6419_6037\Images\travel_icon.png").pixmap(
                QSize(50, 50)
            )
        )
        center_layout.addWidget(plane_icon)

        header_label = QLabel("Join IsraFlight")
        header_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        center_layout.addWidget(header_label)

        # הוספת מרווחים גמישים לפני ואחרי ה-widget המרכזי
        header_layout.addStretch()
        header_layout.addWidget(center_widget)
        header_layout.addStretch()

        main_layout.addWidget(header)

        # Form content
        content = QWidget(self)
        content.setStyleSheet(
            """
            QWidget {
                background-color: white;
            }
            QLineEdit, QDateEdit {
                border: 2px solid #BDC3C7;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                min-height: 20px;
                font-weight: bold;
            }
            QLineEdit:focus, QDateEdit:focus {
                border: 2px solid #4A90E2;
            }
            QLabel {
                font-size: 14px;
                color: #2C3E50;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #3A80D2;
            }
            QCalendarWidget {
                background-color: white;
                color: black;
            }
            QCalendarWidget QToolButton {
                color: black;
                background-color: #E0E0E0;
                border: 1px solid #C0C0C0;
            }
            QCalendarWidget QMenu {
                color: black;
                background-color: white;
            }
            QCalendarWidget QSpinBox {
                color: black;
                background-color: white;
            }
        """
        )
        content_layout = QFormLayout(content)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(15)

        self.username = QLineEdit(self)
        content_layout.addRow("Username:", self.username)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        content_layout.addRow("Password:", self.password)

        self.email = QLineEdit(self)
        content_layout.addRow("Email:", self.email)

        self.first_name = QLineEdit(self)
        content_layout.addRow("First Name:", self.first_name)

        self.last_name = QLineEdit(self)
        content_layout.addRow("Last Name:", self.last_name)

        self.passport_number = QLineEdit(self)
        content_layout.addRow("Passport Number:", self.passport_number)

        self.date_of_birth = QDateEdit(self)
        self.date_of_birth.setDisplayFormat("dd/MM/yyyy")
        self.date_of_birth.setCalendarPopup(True)
        content_layout.addRow("Date of Birth:", self.date_of_birth)

        # יצירת widget לכפתור
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        register_button = QPushButton("Register")
        register_button.setFont(QFont("Arial", 20, QFont.Bold))
        register_button.setFixedHeight(80)
        register_button.setFixedWidth(200)
        register_button.setIcon(
            QIcon(r"IsraelFlight_Fronted_6419_6037\Images\register_icon.png")
        )
        register_button.setIconSize(QSize(24, 24))  # התאם את הגודל לפי הצורך
        register_button.clicked.connect(self.register)

        # מרכוז הכפתור
        button_layout.addStretch()
        button_layout.addWidget(register_button)
        button_layout.addStretch()

        content_layout.addRow(button_widget)

        main_layout.addWidget(content)

    def register(self):
        if not self.validate_input():
            QMessageBox.warning(
                self,
                "Registration Error",
                "Unable to register. Please fill in all required fields.",
            )
            return  # מפסיק את תהליך ההרשמה

        # Here you would typically validate the input and create a new FrequentFlyer object
        # For this example, we'll just accept the dialog
        id = israel_flight_instance.FrequentFlyers[-1].frequentFlyerID + 1
        FrequentFlyer1 = FrequentFlyer(
            id,
            self.username.text(),
            self.password.text(),
            self.email.text(),
            self.first_name.text(),
            self.last_name.text(),
            self.passport_number.text(),
            self.date_of_birth.dateTime().toPython(),
        )
        FrequentFlyerController.add_frequent_flyer(FrequentFlyer1.to_json())
        israel_flight_instance.FrequentFlyers = [
            FrequentFlyer.from_json(FrequentFlyer1)
            for FrequentFlyer1 in FrequentFlyerController.get_frequent_flyers()
        ]
        # self.frequent_flyer_view = FrequentFlyerScreen(FrequentFlyer1)
        # self.frequent_flyer_view.show()
        self.accept()

    def validate_input(self):
        fields_to_check = [
            (self.username, "Username"),
            (self.password, "Password"),
            (self.first_name, "First Name"),
            (self.last_name, "Last Name"),
            (self.passport_number, "Passport Number"),
        ]

        empty_fields = [
            field_name
            for field, field_name in fields_to_check
            if not field.text().strip()
        ]

        if empty_fields:
            error_message = (
                "The following fields are required and cannot be empty:\n- "
                + "\n- ".join(empty_fields)
            )
            QMessageBox.critical(self, "Input Error", error_message)
            return False

        return True
