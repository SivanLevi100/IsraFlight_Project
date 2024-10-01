from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QPushButton, QLabel,
    QScrollArea, QFrame, QGridLayout, QSpacerItem, QDialog, QSizePolicy,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QSize
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from models.IsraelFlight_model import israel_flight_instance
from views.AddPlanetDialog_view import PlaneDialog
from views.EditPlaneDialog_view import EditPlaneDialog
from controllers.plane_controller import PlaneController
from models.Plane_model import Plane

# Main class for displaying individual plane cards
class PlaneCard(QFrame):
    def __init__(self, plane, PlaneListScreen):
        super().__init__()
        self.PlaneListScreen = PlaneListScreen
        self.plane = plane
        self.setup_ui()

    # Set up the user interface for the plane card
    def setup_ui(self):
        # Set up styles and shadow effect
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #E6E6E6;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                background-color: transparent;
            }
            QLabel.field {
                font-weight: bold;
                color: #0047AB;
            }
            QLabel.value {
                color: #333333;
            }
            QPushButton {
                background-color: #0047AB;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #003380;
            }
            QPushButton#deleteButton {
                background-color: transparent;
                padding: 5px;
            }
            QPushButton#deleteButton:hover {
                background-color: rgba(255, 0, 0, 0.1);
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Add delete button
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        delete_button = QPushButton()
        delete_button.setIcon(QIcon("IsraelFlight_Fronted_6419_6037/Images/trash_icon.png"))
        delete_button.setIconSize(QSize(20, 20))
        delete_button.setFixedSize(30, 30)
        delete_button.setObjectName("deleteButton")
        delete_button.clicked.connect(self.delete_plane)
        top_bar.addWidget(delete_button)
        main_layout.addLayout(top_bar)

        # Add image
        self.image_label = QLabel()
        self.image_label.setFixedSize(250, 150)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            background-color: #F0F8FF;
            border-radius: 10px;
            border: 2px solid #E6E6E6;
        """)
        main_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        if self.plane.imageUrl:
            self.load_image(self.plane.imageUrl)

        # Add title
        title = QLabel(f"{self.plane.manufacturer}, {self.plane.model}")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #0047AB; border: none;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Add info layout
        info_widget = QWidget()
        info_widget.setStyleSheet("background-color: transparent; border: none;")
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(8)
        info_layout.setAlignment(Qt.AlignCenter)

        self.add_info_row(info_layout, "ID:", str(self.plane.planeId))
        self.add_info_row(info_layout, "Year:", str(self.plane.yearOfManufacture))
        self.add_info_row(info_layout, "Nickname:", self.plane.nickname or "N/A")

        main_layout.addWidget(info_widget)

        # Add edit button
        edit_button = QPushButton("Edit Plane")
        edit_button.setFixedWidth(120)
        edit_button.clicked.connect(self.edit_plane)
        main_layout.addWidget(edit_button, alignment=Qt.AlignCenter)

    # Add an information row to the layout
    def add_info_row(self, layout, field, value):
        row_layout = QHBoxLayout()
        field_label = QLabel(field)
        field_label.setAlignment(Qt.AlignLeft)
        field_label.setProperty("class", "field")
        field_label.setFixedWidth(80)

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setProperty("class", "value")

        row_layout.addWidget(field_label)
        row_layout.addWidget(value_label)
        layout.addLayout(row_layout)

    # Load the plane image from URL
    def load_image(self, url):
        nam = QNetworkAccessManager(self)
        nam.finished.connect(self.on_image_loaded)
        request = QNetworkRequest(url)
        nam.get(request)

    # Handle the loaded image
    def on_image_loaded(self, reply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            pixmap = QPixmap()
            pixmap.loadFromData(reply.readAll())
            if not pixmap.isNull():
                label_size = self.image_label.size()
                scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                if scaled_pixmap.width() < label_size.width() or scaled_pixmap.height() < label_size.height():
                    empty_pixmap = QPixmap(label_size)
                    empty_pixmap.fill(Qt.transparent)
                    painter = QPainter(empty_pixmap)
                    painter.drawPixmap(
                        (label_size.width() - scaled_pixmap.width()) // 2,
                        (label_size.height() - scaled_pixmap.height()) // 2,
                        scaled_pixmap,
                    )
                    painter.end()
                    self.image_label.setPixmap(empty_pixmap)
                else:
                    self.image_label.setPixmap(scaled_pixmap)
        reply.deleteLater()

    # Open the edit plane dialog
    def edit_plane(self):
        dialog = EditPlaneDialog(self.plane, self.PlaneListScreen)
        if dialog.exec() == QDialog.Accepted:
            self.PlaneListScreen.populate_plane_cards(israel_flight_instance.planes)

    # Delete the plane
    def delete_plane(self):
        confirm_dialog = QMessageBox(self)
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setText("Are you sure you want to delete this plane?")
        confirm_dialog.setWindowTitle("Confirm Deletion")
        confirm_dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm_dialog.setDefaultButton(QMessageBox.Cancel)

        result = confirm_dialog.exec()
        confirm_dialog.hide()

        if result == QMessageBox.Ok:
            try:
                associated_flights = [
                    flight for flight in israel_flight_instance.Flights
                    if flight.PlaneId == self.plane.planeId
                ]

                if associated_flights:
                    flight_ids = ", ".join([str(flight.FlightId) for flight in associated_flights])
                    QMessageBox.warning(
                        self,
                        "Cannot Delete",
                        f"This plane cannot be deleted because it is associated with the following flights: {flight_ids}. Please remove these flights first.",
                    )
                else:
                    PlaneController.delete_plane(self.plane.planeId)
                    israel_flight_instance.planes = [
                        Plane.from_json(plane_data)
                        for plane_data in PlaneController.get_planes()
                    ]

                    self.PlaneListScreen.populate_plane_cards(israel_flight_instance.planes)

                    QMessageBox.information(self, "Success", "The plane has been deleted successfully.")
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Could not delete the plane. It may have already been removed.",
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"An error occurred while deleting the plane: {str(e)}",
                )