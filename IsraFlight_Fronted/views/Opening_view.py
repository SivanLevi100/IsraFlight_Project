from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, 
    QFrame, QToolButton, QSizePolicy, QGridLayout, QSpacerItem,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QImage
from views.Admin_view import AdminScreen
from views.login_frequent_flyer_view import LoginFrequentFlyerScreen

# Main class for the opening screen of the application
class OpeningScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Israel Flight")
        self.setGeometry(500, 200, 800, 600)
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setWindowIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\logo_icon.png"))
        self.init_ui()

    # Initialize the user interface
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 30, 50, 20)

        # Header with settings and help buttons
        header_layout = QHBoxLayout()
        settings_btn = QPushButton()
        settings_btn.setIcon(QIcon("IsraelFlight_Fronted_6419_6037\Images\settings_icon.png"))
        settings_btn.setIconSize(QSize(50, 50))
        settings_btn.setFixedSize(50, 50)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.7);
                border: 2px solid #FFFFFF;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: rgba(230, 242, 255, 0.7);
            }
        """)
        header_layout.addWidget(settings_btn, alignment=Qt.AlignLeft)
        header_layout.addStretch()

        help_btn = QPushButton()
        help_btn.setIcon(QIcon("IsraelFlight_Fronted_6419_6037\Images\help_icon.png"))
        help_btn.setIconSize(QSize(50, 50))
        help_btn.setFixedSize(50, 50)
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.7);
                border: 2px solid #FFFFFF;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: rgba(230, 242, 255, 0.7);
            }
        """)
        header_layout.addWidget(help_btn, alignment=Qt.AlignRight)

        # Logo
        logo = QLabel(self)
        logo.setPixmap(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\IsraelFlight_logo.png").pixmap(QSize(600, 600)))
        logo.setAlignment(Qt.AlignCenter)

        # Subtitle
        subtitle = QLabel("  Your gateway to seamless travel experiences")
        subtitle.setFont(QFont("Arial", 25, QFont.Bold))
        subtitle.setStyleSheet("color: #4a90e2;")
        subtitle.setAlignment(Qt.AlignCenter)

        # Icons and buttons layout
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # Admin layout: icon + button vertically aligned
        admin_layout = QVBoxLayout()
        admin_icon = QLabel()
        admin_icon.setPixmap(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\Admin_icon.png").pixmap(QSize(120, 120)))
        self.admin_btn = self.create_styled_button("Admin","#004AAD", "#012F6D")
        admin_layout.addWidget(admin_icon, alignment=Qt.AlignCenter)
        admin_layout.addWidget(self.admin_btn, alignment=Qt.AlignCenter)

        # Frequent Flyer layout: icon + button vertically aligned
        frequent_flyer_layout = QVBoxLayout()
        frequent_flyer_icon = QLabel()
        frequent_flyer_icon.setPixmap(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\user_icon.png").pixmap(QSize(120, 120)))
        self.frequent_flyer_btn = self.create_styled_button("Frequent Flyer", "#1E90FF", "#1873CC")
        frequent_flyer_layout.addWidget(frequent_flyer_icon, alignment=Qt.AlignCenter)
        frequent_flyer_layout.addWidget(self.frequent_flyer_btn, alignment=Qt.AlignCenter)

        # Add admin and frequent flyer layouts to the grid
        grid_layout.addLayout(admin_layout, 0, 0, Qt.AlignCenter)
        grid_layout.addLayout(frequent_flyer_layout, 0, 1, Qt.AlignCenter)
        self.admin_btn.clicked.connect(self.open_admin_screen)
        self.frequent_flyer_btn.clicked.connect(self.open_frequentFlyer_screen)

        # Adjust column stretch factors for proper spacing
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)

        # Footer information
        footer_layout = QHBoxLayout()
        footer_info = QLabel("Version 1.0.3   |   © 2024 Israel Flight   |   support@israelflight.com   |   Tel: +972-3-1234567   |   Terms of Service   |   Privacy Policy  ")
        footer_info.setAlignment(Qt.AlignCenter)
        footer_info.setStyleSheet("color: #2980B9;; font-size: 14px; font-weight: bold;")
        footer_layout.addWidget(footer_info)

        # Add widgets to main layout
        main_layout.addLayout(header_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(logo)
        main_layout.addWidget(subtitle)
        main_layout.addStretch(1)
        main_layout.addLayout(grid_layout)
        main_layout.addStretch(2)
        main_layout.addWidget(QFrame(frameShape=QFrame.HLine, styleSheet="background-color: #CCCCCC;"))
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

    # Create a styled button with custom colors
    def create_styled_button(self, text, base_color, hover_color):
        btn = QPushButton(text)
        btn.setFont(QFont("Arial", 16, QFont.Bold))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color}; 
                color: white; 
                padding: 15px 30px; 
                border-radius: 25px;
                border: none;
                min-width: 220px;
                max-width: 250px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)
        return btn

    # Paint event to set background color
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255))  # White background

    # Open the admin screen
    def open_admin_screen(self):
        self.admin_screen = AdminScreen(self)
        self.admin_screen.show()
        self.close()
        print("Opening Admin Screen")

    # Open the frequent flyer screen
    def open_frequentFlyer_screen(self):
        self.LoginFrequentFlyer_screen = LoginFrequentFlyerScreen(self)
        self.LoginFrequentFlyer_screen.show()
        self.close()
        print("Opening Frequent Flyer Screen")