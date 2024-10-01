from PySide6.QtWidgets import (QApplication, QWidget, QFrame, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout,
                               QScrollArea, QDialog)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon
from models.IsraelFlight_model import israel_flight_instance
from views.frequent_flyer_view import FrequentFlyerScreen
from views.register_view import RegisterDialog

# Main class for the Frequent Flyer Login Screen
class LoginFrequentFlyerScreen(QWidget):
    def __init__(self, homeScreen):
        super().__init__()
        self.setWindowIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\logo_icon.png"))
        self.setWindowTitle("IsraFlight - Frequent Flyer Login")
        self.setGeometry(100, 100, 1200, 800)
        self.showMaximized()

        self.homeScreen = homeScreen

        # Set application-wide font
        app_font = QFont("Arial", 10)
        QApplication.setFont(app_font)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)
        content_layout.setContentsMargins(0, 50, 0, 50)
        self.create_login_form(content_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)
        scroll_area.setStyleSheet("background-color: #FFFFFF;")
        main_layout.addWidget(scroll_area)

        bottom_bar = self.create_bottom_bar()
        main_layout.addWidget(bottom_bar)

    # Create the top bar of the login screen
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
        logo_label.setPixmap(QIcon("IsraelFlight_Fronted_6419_6037\Images\IsraelFlight_logo.png").pixmap(QSize(200,200)))
        logo_label.setStyleSheet("""
            border: None 
        """)
        
        top_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        title_label = QLabel("Log In ")
        title_label.setStyleSheet("""
            font-size: 35px;
            font-weight: bold;
            color: #2980B9;
            border: None 
        """)
        title_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(title_label)

        home_button = QPushButton()
        home_button.setIcon(QIcon("IsraelFlight_Fronted_6419_6037\Images\home_icon.png"))
        home_button.setIconSize(QSize(32, 32))
        home_button.setFixedSize(50, 50)

        home_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.7);
                border: 2px solid #4a90e2;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: rgba(230, 242, 255, 0.7);
            }
        """)
        home_button.clicked.connect(self.go_to_home_screen)

        top_layout.addWidget(home_button, alignment=Qt.AlignRight)

        return top_bar

    # Create the login form
    def create_login_form(self, layout):
        form_widget = QWidget()
        form_widget.setFixedWidth(400)
        form_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 40px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
        """)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)

        # Welcome text
        welcome_label = QLabel("Welcome to IsraFlight")
        welcome_label.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: #003366;
            margin-bottom: 20px;
        """)
        welcome_label.setFixedWidth(400)
        welcome_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(welcome_label)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #B0C4DE;
                border-radius: 18px;
                padding: 14px;
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border: 3px solid #4682B4;
            }
        """)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #B0C4DE;
                border-radius: 18px;
                padding: 14px;
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border: 3px solid #4682B4;
            }
        """)

        # Login button
        login_button = QPushButton(" Log In")
        login_button.clicked.connect(self.login)
        login_button.setIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\lock_icon.png"))
        login_button.setIconSize(QSize(35, 35))
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #003366;
                color: white;
                border: none;
                border-radius: 18px;
                padding: 16px;
                font-size: 21px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #004080;
            }
        """)
        login_button.setFixedHeight(55)

        # Register link
        register_link = QPushButton("Don't have an account? Sign up")
        register_link.clicked.connect(self.open_register_dialog)
        register_link.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                color: #4682B4;
                text-decoration: underline;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #4169E1;
            }
        """)

        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_button)
        form_layout.addWidget(register_link)

        layout.addWidget(form_widget, alignment=Qt.AlignCenter)

    # Create the bottom bar of the login screen
    def create_bottom_bar(self):
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet("""
            QFrame {
                background-color: #34495E;
            }
        """)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(20, 15, 20, 15)

        footer_text = QLabel("Version 1.0.3   |   © 2024 Israel Flight   |   support@israelflight.com   |   Tel: +972-3-1234567   |   Terms of Service   |   Privacy Policy  ")
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setStyleSheet("""
            color: #FFFFFF;
            font-size: 13px;
            font-weight: bold
        """)
        bottom_layout.addWidget(footer_text)

        return bottom_bar

    # Navigate back to the home screen
    def go_to_home_screen(self):
        self.homeScreen.show()
        self.close()

    # Handle the login process
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user_found = False
        for FrequentFlyer in israel_flight_instance.FrequentFlyers:
            if FrequentFlyer.username == username and FrequentFlyer.passwordHash == password:
                user_found = True
                
                # Create a custom styled message box
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Login Successful")
                msg_box.setText(f"Welcome, {username}!")
                msg_box.setIcon(QMessageBox.Information)
                
                # Style the message box
                msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: #F0F4F8;
                    }
                    QLabel {
                        color: #2C3E50;
                        font-size: 14px;
                    }
                    QPushButton {
                        background-color: #3498DB;
                        color: white;
                        padding: 5px 15px;
                        border-radius: 3px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #2980B9;
                    }
                """)
                
                # Set custom font for the text
                font = QFont("Arial", 12)
                msg_box.setFont(font)
                
                # Show the message box
                msg_box.exec()
                
                self.FrequentFlyer_screen = FrequentFlyerScreen(FrequentFlyer, self)
                self.FrequentFlyer_screen.show()
                self.close()
                break

        if not user_found:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    # Open the registration dialog
    def open_register_dialog(self):
        register_dialog = RegisterDialog(self)
        if register_dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Registration Successful", "Your account has been created successfully! Please log in with your new credentials.")