from datetime import datetime
import sys
from PySide6.QtWidgets import (QApplication, QFrame, QSizePolicy, QHeaderView, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel,QGraphicsDropShadowEffect, QDialog, QMessageBox, QScrollArea, QComboBox)
from PySide6.QtGui import QFont, QPixmap, QIcon, QColor, QPainter, QPainterPath
from PySide6.QtCore import Qt, QSize, QRect, QPoint
from models.FrequentFlyer_model import FrequentFlyer
from models.Booking_model import Booking
from controllers.booking_Controller import BookingController
from controllers.services_controller import HebcalController
from views.MyBooking_view import MyBookingsWindow
import random
from models.IsraelFlight_model import israel_flight_instance
from controllers.FlightDelayPredictionController import FlightDelayPredictionController

# Main class for displaying a flight card
class FlightCard(QWidget):
    def __init__(self, flight, FrequentFlyerScreen):
        super().__init__()
        self.flight = flight
        self.FrequentFlyerScreen = FrequentFlyerScreen
        self.initUI()

    # Initialize the user interface for the flight card
    def initUI(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(180)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            FlightCard {
                background-color: #FFFFFF;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
            }
            QLabel {
                color: #333333;
                background-color: #FFFFFF;
            }
        """)

        # Add subtle drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Left section - Flight number and basic info
        left_layout = QVBoxLayout()
        Company_flight_icon = QLabel()
        Company_flight_icon.setPixmap(QIcon("IsraelFlight_Fronted_6419_6037/Images/IsraelFlight_logo.png").pixmap(QSize(80,80)))
        left_layout.addWidget(Company_flight_icon)
        
        # flight ID
        flight_id = QLabel(f"Flight ID: {self.flight.FlightId}")
        flight_id.setFont(QFont("Arial", 12, QFont.Bold))
        flight_id.setStyleSheet("color: #1A5F7A;")
        left_layout.addWidget(flight_id)

        # Is_Delayed flight
        occupancy = self.count_flight_bookings(self.flight.FlightId)
        plane_nickname = self.find_plane_nickname(self.flight.PlaneId)
        DepartureHour = self.flight.DepartureDateTime.strftime('%H')  # Extract hour
        day_of_week = (self.flight.DepartureDateTime.weekday() + 1) % 7  # Extract full day name of the week - where 0 refers to Sunday and 6 to Saturday
        departure_Location = self.flight.DepartureLocation
        print(f"Occupancy: {occupancy}, Plane Nickname: {plane_nickname}, Departure Hour: {DepartureHour}, Day of Week: {day_of_week}, Departure Location: {departure_Location}")

        flight_data = FlightDelayPredictionController().format_flight_data(occupancy, plane_nickname, 
                                                                         DepartureHour, day_of_week, departure_Location)
        Is_Delayed = FlightDelayPredictionController().predict_delay(flight_data)
        print(Is_Delayed)
        if Is_Delayed["delay_prediction"] == "Delayed":
            Color = "color: #C20000;"
        else:
            Color = "color: #000CC2;"
        Is_Delayed_label = QLabel(f"{Is_Delayed['delay_prediction']}")
        Is_Delayed_label.setFont(QFont("Arial", 12, QFont.Bold))
        Is_Delayed_label.setStyleSheet(Color)
        left_layout.addWidget(Is_Delayed_label)
        
        left_layout.addStretch()
        main_layout.addLayout(left_layout)

        # Middle section - Departure and Arrival details
        middle_layout = QVBoxLayout()
        
        # Departure
        departure_layout = QHBoxLayout()
        departure_icon = QLabel()
        departure_icon.setPixmap(QIcon("IsraelFlight_Fronted_6419_6037\Images\departures_icon.png").pixmap(QSize(45, 45)))
        departure_icon.setAlignment(Qt.AlignCenter) 
        departure_layout.addWidget(departure_icon)

        departure_info_layout = QVBoxLayout()
        departure_location = QLabel(self.flight.DepartureLocation)
        departure_location.setFont(QFont("Arial", 13, QFont.Bold))
        departure_location.setStyleSheet("color: #1A5F7A; ")
        departure_info_layout.addWidget(departure_location)
        departure_location.setAlignment(Qt.AlignCenter) 

        departure_datetime = QLabel(f"{self.flight.DepartureDateTime.strftime('%Y-%m-%d')} | {self.flight.DepartureDateTime.strftime('%H:%M')}")
        departure_datetime.setFont(QFont("Arial", 12,QFont.Bold))
        departure_datetime.setStyleSheet("color: #333333; background-color: #FFFFFF;")
        departure_info_layout.addWidget(departure_datetime)

        departure_info_layout.setAlignment(Qt.AlignCenter) 
        departure_layout.addLayout(departure_info_layout) 
        middle_layout.addLayout(departure_layout)
       
        # Separator
        separator = QLabel()
        separator.setFixedHeight(2)
        separator.setStyleSheet("background-color: #E0E0E0;")
        middle_layout.addWidget(separator)

        # Arrival
        arrival_layout = QHBoxLayout()
        arrival_icon = QLabel()
        arrival_icon.setPixmap(QIcon("IsraelFlight_Fronted_6419_6037\Images\Arrivals_icon.png").pixmap(QSize(45, 45)))
        arrival_icon.setAlignment(Qt.AlignCenter) 
        arrival_layout.addWidget(arrival_icon)
        
        arrival_info_layout = QVBoxLayout()
        arrival_location = QLabel(self.flight.LandingLocation)
        arrival_location.setFont(QFont("Arial", 13, QFont.Bold))
        arrival_location.setStyleSheet("color: #1A5F7A; ")
        arrival_location.setAlignment(Qt.AlignCenter) 
        arrival_info_layout.addWidget(arrival_location)
       
        arrival_datetime = QLabel(f"{self.flight.EstimatedLandingDateTime.strftime('%Y-%m-%d')} | {self.flight.EstimatedLandingDateTime.strftime('%H:%M')}")
        arrival_datetime.setFont(QFont("Arial", 12,QFont.Bold))
        arrival_datetime.setStyleSheet("color: #333333; background-color: #FFFFFF;")
        arrival_info_layout.addWidget(arrival_datetime)
        
        arrival_info_layout.setAlignment(Qt.AlignCenter) 
        arrival_layout.addLayout(arrival_info_layout)
        
        middle_layout.addLayout(arrival_layout)

        main_layout.addLayout(middle_layout, 1)  # Give more space to the middle section

        # Right section - Price and booking
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        price_label = QLabel(f"${self.flight.FlightPrice:.2f}")
        price_label.setFont(QFont("Arial", 20, QFont.Bold))
        price_label.setStyleSheet("color: #1A5F7A;")
        price_label.setAlignment(Qt.AlignCenter) 
        right_layout.addWidget(price_label)

        book_button = QPushButton("Book Now")
        book_button.setFont(QFont("Arial", 12, QFont.Bold))
        book_button.setStyleSheet("""
            QPushButton {
                background-color: #1A5F7A;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #2E8BC0;
            }
        """)
        book_button.clicked.connect(self.on_book_clicked)
        right_layout.addWidget(book_button)

        main_layout.addLayout(right_layout)

    # Custom paint event to draw the rounded rectangle background
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw main background
        path = QPainterPath()
        path.addRoundedRect(QRect(0, 0, self.width(), self.height()), 10, 10)
        painter.fillPath(path, QColor("#FFFFFF"))

    # Handle the book button click event
    def on_book_clicked(self):
        self.FrequentFlyerScreen.show_flight_details(self.flight)
        
    # Functions for flight delay prediction

    # Calculate occupancy of the flight
    def count_flight_bookings(self, flight_id: int):
        booking_count = len([booking for booking in israel_flight_instance.Bookings if booking.flightId == flight_id])
    
        if booking_count > 4:
            occupancy = 'full'
        elif 2 <= booking_count <= 3:
            occupancy = 'partial'
        else:
            occupancy = 'minimal'
    
        return occupancy

    # Find the plane nickname based on the plane ID
    def find_plane_nickname(self, plane_Id: int):
        plane = next((p for p in israel_flight_instance.planes if p.planeId == plane_Id), None)
        if plane is None:
            return "Plane not found"
        return plane.nickname