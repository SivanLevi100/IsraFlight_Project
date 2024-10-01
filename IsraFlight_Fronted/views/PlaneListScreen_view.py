from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QGridLayout, QMessageBox, QFrame, QScrollArea,
    QHeaderView, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QDialog, QSpacerItem, QSizePolicy,
)
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from models.IsraelFlight_model import israel_flight_instance
from views.AddPlanetDialog_view import PlaneDialog
from views.EditPlaneDialog_view import EditPlaneDialog
from views.PlaneCard_view import PlaneCard
from controllers.plane_controller import PlaneController
from models.Plane_model import Plane

# Main class for displaying the list of planes
class PlaneListScreen(QWidget):
    def __init__(self, home_screen):
        super().__init__()
        self.home_screen = home_screen
        self.setup_ui()
        self.populate_plane_cards(israel_flight_instance.planes)

    # Set up the user interface
    def setup_ui(self):
        self.setWindowIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\logo_icon.png"))
        self.setWindowTitle("Planes Management")
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
                background-color: #4D9FFF;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.create_top_bar())

        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(30, 30, 30, 30)

        # Add Plane button
        add_plane_button = QPushButton("  Add Plane")
        add_plane_button.setFont(QFont("Arial", 18))
        add_plane_button.setFixedSize(150, 40)
        add_plane_button.setIcon(QIcon("IsraelFlight_Fronted_6419_6037/Images/plus_icon.png"))
        add_plane_button.setIconSize(QSize(20, 20))
        add_plane_button.clicked.connect(self.add_plane)
        add_plane_button.setStyleSheet("""
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
        """)
        content_layout.addWidget(add_plane_button, alignment=Qt.AlignRight)

        # Grid for plane cards
        self.plane_grid = QGridLayout()
        self.plane_grid.setSpacing(20)
        content_layout.addLayout(self.plane_grid)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        main_layout.addWidget(self.create_bottom_bar())

    # Create the top bar of the screen
    def create_top_bar(self):
        top_bar = QFrame()
        top_bar.setStyleSheet("""
        QFrame {
            background-color: #FFFFFF;
            border-bottom: 2px solid #0047AB;
        }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 10, 20, 10)

        logo_label = QLabel()
        logo_label.setPixmap(QIcon("IsraelFlight_Fronted_6419_6037\Images\IsraelFlight_logo.png").pixmap(QSize(150, 150)))
        logo_label.setStyleSheet("border: None;")
        top_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        title_label = QLabel("Planes Management")
        title_label.setStyleSheet("""
        font-size: 35px;
        font-weight: bold;
        color: #0047AB;
        border: None;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(title_label, 1)

        # Home button on the right
        home_button = QPushButton()
        home_button.setIcon(
            QIcon("IsraelFlight_Fronted_6419_6037\Images\home_icon.png")
        )
        home_button.setIconSize(QSize(32, 32))
        home_button.setFixedSize(50, 50)
        home_button.setStyleSheet(
            """
        QPushButton {
            background-color: white;
            border: 2px solid #0047AB;
            border-radius: 25px;
        }
        QPushButton:hover {
            background-color: #E6F2FF;
        }
    """
        )
        home_button.clicked.connect(self.go_to_home_screen)
        top_layout.addWidget(home_button, alignment=Qt.AlignRight)

        return top_bar

    def create_bottom_bar(self):
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet(
            """
            QFrame {
                background-color: #34495E;
                border: none;
            }
        """
        )

        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(20, 10, 20, 10)

        footer_text = QLabel(
            "Version 1.0.3   |   © 2024 Israel Flight   |   support@israelflight.com   |   Tel: +972-3-1234567   |   Terms of Service   |   Privacy Policy   "
        )
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setStyleSheet(
            """
            color: #FFFFFF;
            font-size: 13px;
            font-weight: bold;
        """
        )
        bottom_layout.addWidget(footer_text)

        return bottom_bar

    def go_to_home_screen(self):
        self.home_screen.show()
        self.close()

    def populate_plane_cards(self, planes):
        # Clear existing items
        for i in reversed(range(self.plane_grid.count())):
            widget = self.plane_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        row, col = 0, 0
        for plane in planes:
            card = PlaneCard(plane, self)
            self.plane_grid.addWidget(card, row, col)
            col += 1
            if col > 2:  # Adjust this value to change the number of columns
                col = 0
                row += 1

        # Add stretch to fill empty space
        self.plane_grid.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding),
            row + 1,
            0,
            1,
            3,
        )

    def add_plane(self):
        dialog = PlaneDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.populate_plane_cards(israel_flight_instance.planes)


