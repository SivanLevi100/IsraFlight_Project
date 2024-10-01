from datetime import datetime
import sys
from PySide6.QtWidgets import QApplication, QFrame, QSizePolicy, QCalendarWidget, QHeaderView, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QMessageBox, QScrollArea, QComboBox
from PySide6.QtGui import QFont, QPixmap, QIcon, QColor
from PySide6.QtCore import Qt, QSize, QDate
from models.FrequentFlyer_model import FrequentFlyer
from models.Booking_model import Booking
from controllers.booking_Controller import BookingController
from controllers.services_controller import HebcalController
from views.MyBooking_view import MyBookingsWindow
import random
from views.FlightCard_view import FlightCard
from models.IsraelFlight_model import israel_flight_instance

TIME_FILTERS = {
   "All": (None, None),
    "Morning: 6:00 - 12:00": (6, 12),
    "Afternoon: 12:00 - 18:00": (12, 18),
    "Evening: 18:00 - 00:00": (18, 24),
    "Night: 00:00 - 6:00": (0, 6)
}

# Main class for the Frequent Flyer dashboard
class FrequentFlyerScreen(QWidget):
    def __init__(self, frequentFlyer, login_screen):
        super().__init__()
        self.frequentFlyer = frequentFlyer
        self.login_screen = login_screen
        self.current_view = 'departure'
        
        self.initUI()

    # Initialize the user interface
    def initUI(self):
        self.setWindowIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\logo_icon.png"))
        self.setWindowTitle("IsraFlight - Frequent Flyer Dashboard")
        self.showMaximized()
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F7FA;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #2C3E50;
            }
            QScrollBar:vertical {
                border: none;
                background: #E0E6ED;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #7F8C8D;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.create_top_bar())

        self.content_widget = self.create_content_area()
        main_layout.addWidget(self.content_widget)

        main_layout.addWidget(self.create_bottom_bar())

        self.show_takeoff_flights()

    # Create the top bar of the dashboard
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
        logo_label.setPixmap(QIcon("IsraelFlight_Fronted_6419_6037/Images/IsraelFlight_logo.png").pixmap(QSize(200,200)))
        logo_label.setStyleSheet("""
            border: None 
        """)
        top_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        title_label = QLabel("Our Available Flights ")  
        title_label.setStyleSheet("""
            font-size: 35px;
            font-weight: bold;
            color: #2980B9;
            border: None 
        """)      
        title_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(title_label, alignment=Qt.AlignCenter)  

        logout_button = QPushButton()
        logout_button.setIcon(QIcon("IsraelFlight_Fronted_6419_6037\Images\logout_icon.png"))
        logout_button.setIconSize(QSize(40, 40))
        logout_button.setFixedSize(40, 40)
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: none;
            }
            QPushButton:hover {
                  background-color: #E0E0E0;
               }
            QPushButton:pressed {
                  background-color: #BDBDBD;
             }
                  """)
        logout_button.clicked.connect(self.go_to_home_screen)
        top_layout.addWidget(logout_button, alignment=Qt.AlignRight)

        return top_bar

    # Create the main content area of the dashboard
    def create_content_area(self):
        content_scroll_area = QScrollArea()
        content_scroll_area.setWidgetResizable(True)
        content_scroll_area.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        self.content_layout.setSpacing(30)
        self.content_layout.setAlignment(Qt.AlignTop)

        welcome_label = QLabel(f"Welcome, {self.frequentFlyer.firstName} {self.frequentFlyer.lastName}")
        welcome_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: #34495E; margin-bottom: 20px;")
        self.content_layout.addWidget(welcome_label)

        self.content_layout.addLayout(self.create_button_layout())
        self.content_layout.addLayout(self.create_filter_layout())

        self.flights_layout = QVBoxLayout()
        self.flights_layout.setAlignment(Qt.AlignCenter)
        self.content_layout.addLayout(self.flights_layout)

        content_scroll_area.setWidget(content_widget)
        return content_scroll_area

    # Create the button layout for navigation
    def create_button_layout(self):
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        self.takeoff_button = self.create_styled_button(" Flights From TLV", "#3498DB", is_main=True)
        self.takeoff_button.setIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\From_tlv_icon.png"))
        self.takeoff_button.setIconSize(QSize(28, 28))
        self.takeoff_button.clicked.connect(self.show_takeoff_flights)
        button_layout.addWidget(self.takeoff_button)

        self.landing_button = self.create_styled_button(" Flights To TLV", "#164462", is_main=True)
        self.landing_button.setIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\To_tlv_icon.png"))
        self.landing_button.setIconSize(QSize(28, 28))
        self.landing_button.clicked.connect(self.show_landing_flights)
        button_layout.addWidget(self.landing_button)

        button_layout.addStretch()

        self.my_booking_button = self.create_styled_button("My Bookings", "#E74C3C", is_main=False)
        self.my_booking_button.clicked.connect(self.show_my_bookings)
        button_layout.addWidget(self.my_booking_button)

        return button_layout

    # Create the filter layout for time and date filtering
    def create_filter_layout(self):
        filter_layout = QHBoxLayout()
        
        # Time filter
        time_filter_layout = QVBoxLayout()
        filter_label = QLabel("Filter by time:")
        filter_label.setFont(QFont("Segoe UI", 14))
        self.time_filter = QComboBox()
        self.time_filter.addItems(["All", "Morning: 6:00 - 12:00", "Afternoon: 12:00 - 18:00", "Evening: 18:00 - 00:00", "Night: 00:00 - 6:00"])
        self.time_filter.setFont(QFont("Segoe UI", 12))
        self.time_filter.setFixedWidth(200)
        self.time_filter.setStyleSheet("""
            QComboBox {
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #BDC3C7;
            }
        """)
        self.time_filter.currentTextChanged.connect(self.apply_filter)
        time_filter_layout.addWidget(filter_label)
        time_filter_layout.addWidget(self.time_filter)
        
        # Date filter
        date_filter_layout = QVBoxLayout()
        date_label = QLabel("Filter by date:")
        date_label.setFont(QFont("Segoe UI", 14))
        self.date_filter = QPushButton("Select Date")
        self.date_filter.setFont(QFont("Segoe UI", 12))
        self.date_filter.setFixedWidth(150)
        self.date_filter.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                padding: 5px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
        """)
        self.date_filter.clicked.connect(self.show_calendar)
        date_filter_layout.addWidget(date_label)
        date_filter_layout.addWidget(self.date_filter)
        
        filter_layout.addLayout(time_filter_layout)
        filter_layout.addLayout(date_filter_layout)
        filter_layout.addStretch()
        
        # Reset button
        reset_button = QPushButton()
        reset_button.setIcon(QIcon("IsraelFlight_Fronted_6419_6037/Images/reset_icon.png"))
        reset_button.setIconSize(QSize(24, 24))
        reset_button.setFixedSize(40, 40)
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                  background-color: #E0E0E0;
               }
            QPushButton:pressed {
                  background-color: #BDBDBD;
             }
                  """)
        reset_button.clicked.connect(self.reset_filters)
        filter_layout.addWidget(reset_button)
        
        return filter_layout

    # Create a styled button
    def create_styled_button(self, text, color, is_main=True):
        button = QPushButton(text)
        button.setFont(QFont("Segoe UI", 14, QFont.Medium))
        if is_main:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setFixedSize(230, 40)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #FFFFFF;
                    color:{color};
                    border: 2px solid {color};
                    border-radius: 20px;
                    padding: 5px 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: white;
                }}
            """)
        else:
            button.setFixedSize(150, 40)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: white;
                    color: {color};
                    border: 2px solid {color};
                    border-radius: 10px;
                    padding: 5px 10px;
                    font-weight: bold;
                    font-size: 15px
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: white;
                }}
            """)
        return button

    # Static method to lighten a color
    @staticmethod
    def lighten_color(color):
        c = QColor(color)
        h, s, l, _ = c.getHslF()
        return QColor.fromHslF(h, s, min(1.0, l * 1.2), 1.0).name()

    # Populate the flights area with flight cards
    def populate_flights(self, flights, location_type, target_location):
        # Clear existing items in the flights_layout
        for i in reversed(range(self.flights_layout.count())):
            widget = self.flights_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        filtered_flights = [flight for flight in flights if getattr(flight, location_type) == target_location]

        # Create a new widget to hold the centered content
        centered_widget = QWidget()
        centered_layout = QVBoxLayout(centered_widget)
        centered_layout.setAlignment(Qt.AlignCenter)

        if filtered_flights:
            for index, flight in enumerate(filtered_flights):
                flight_card = FlightCard(flight, self)
                centered_layout.addWidget(flight_card)
        else:
            no_flights_label = QLabel("No flights available for the selected time range.")
            no_flights_label.setFont(QFont("Segoe UI", 16))
            no_flights_label.setStyleSheet("color: #7F8C8D;")
            no_flights_label.setAlignment(Qt.AlignCenter)
            centered_layout.addWidget(no_flights_label)

        # Add the centered widget to the flights_layout
        self.flights_layout.addWidget(centered_widget)
        self.flights_layout.setAlignment(Qt.AlignCenter)

    def show_takeoff_flights(self):
        self.current_view = 'departure'
        self.takeoff_button.setStyleSheet(self.takeoff_button.styleSheet().replace("background-color: #3498DB", "background-color: #2980B9"))
        self.landing_button.setStyleSheet(self.landing_button.styleSheet().replace("background-color: #2980B9", "background-color: #2ECC71"))
        self.apply_filter()

    def show_landing_flights(self):
        self.current_view = 'arrival'
        self.landing_button.setStyleSheet(self.landing_button.styleSheet().replace("background-color: #2ECC71", "background-color: #27AE60"))
        self.takeoff_button.setStyleSheet(self.takeoff_button.styleSheet().replace("background-color: #2980B9", "background-color: #3498DB"))
        self.apply_filter()

    def show_landing_flights(self):
        self.current_view = 'arrival'
        self.landing_button.setStyleSheet(self.landing_button.styleSheet().replace("background-color: #2ECC71", "background-color: #27AE60"))
        self.takeoff_button.setStyleSheet(self.takeoff_button.styleSheet().replace("background-color: #2980B9", "background-color: #3498DB"))
        self.apply_filter()

    def show_calendar(self):
        calendar = QCalendarWidget(self)
        calendar.setGridVisible(True)
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        calendar.setStyleSheet("""
    /* Main Calendar Widget */
    QCalendarWidget {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 5px;
    }

    /* Navigation bar */
    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #F5F5F5;
        border-bottom: 1px solid #E0E0E0;
    }

    /* Month/Year labels */
    QCalendarWidget QToolButton {
        color: #2C3E50;
        background-color: transparent;
        border: none;
        border-radius: 4px;
        padding: 6px;
        font-weight: bold;
    }

    QCalendarWidget QToolButton:hover {
        background-color: #ECF0F1;
    }

    QCalendarWidget QToolButton::menu-indicator {
        image: none;
    }

    /* Days of week header */
    QCalendarWidget QWidget { 
        alternate-background-color: #F9F9F9; 
    }

    /* Date grid */
    QCalendarWidget QAbstractItemView:enabled {
        color: #2C3E50;
        background-color: #FFFFFF;
        selection-background-color: #3498DB;
        selection-color: #FFFFFF;
        border: none;
    }

    QCalendarWidget QAbstractItemView:disabled {
        color: #BDC3C7;
    }

    /* Today date */
    QCalendarWidget QAbstractItemView:enabled:selected {
        background-color: #2980B9;
    }

    /* Hovered date */
    QCalendarWidget QAbstractItemView:enabled:hover {
        background-color: #E0F2FE;
        border: 1px solid #3498DB;
    }

    /* Navigation arrows */
    QCalendarWidget QToolButton::right-arrow {
        image: url(right_arrow.png);
    }

    QCalendarWidget QToolButton::left-arrow {
        image: url(left_arrow.png);
    }

    QCalendarWidget QToolButton::right-arrow:hover,
    QCalendarWidget QToolButton::left-arrow:hover {
        background-color: #ECF0F1;
    }

    /* Spin box for year selection */
    QCalendarWidget QSpinBox {
        color: #2C3E50;
        background-color: #FFFFFF;
        selection-background-color: #3498DB;
        selection-color: #FFFFFF;
        border: 1px solid #BDC3C7;
        border-radius: 3px;
        padding: 2px;
    }
""")
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Date")
        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.addWidget(calendar)
        
        def on_date_selected():
            selected_date = calendar.selectedDate()
            self.date_filter.setText(selected_date.toString("yyyy-MM-dd"))
            dialog.accept()
            self.apply_filter()
        
        calendar.clicked.connect(on_date_selected)
        
        dialog.exec()
    def apply_filter(self):
        time_filter = self.time_filter.currentText()
        date_filter = self.date_filter.text()
        
        start_hour, end_hour = TIME_FILTERS.get(time_filter, (None, None))
        
        if self.current_view == 'departure':
            filtered_flights = israel_flight_instance.Flights
            if start_hour is not None and end_hour is not None:
                filtered_flights = [
                    flight for flight in filtered_flights 
                    if start_hour <= flight.DepartureDateTime.hour < end_hour
                ]
            if date_filter != "Select Date":
                filter_date = QDate.fromString(date_filter, "yyyy-MM-dd")
                filtered_flights = [
                    flight for flight in filtered_flights
                    if flight.DepartureDateTime.date() == filter_date.toPython()
                ]
            self.populate_flights(filtered_flights, 'DepartureLocation', 'TLV')
        
        elif self.current_view == 'arrival':
            filtered_flights = israel_flight_instance.Flights
            if start_hour is not None and end_hour is not None:
                filtered_flights = [
                    flight for flight in filtered_flights 
                    if start_hour <= flight.EstimatedLandingDateTime.hour < end_hour
                ]
            if date_filter != "Select Date":
                filter_date = QDate.fromString(date_filter, "yyyy-MM-dd")
                filtered_flights = [
                    flight for flight in filtered_flights
                    if flight.EstimatedLandingDateTime.date() == filter_date.toPython()
                ]
            self.populate_flights(filtered_flights, 'LandingLocation', 'TLV')
        
        else:
            self.populate_flights(israel_flight_instance.Flights, 'DepartureLocation', 'TLV')

    def reset_filters(self):
        self.time_filter.setCurrentText("All")
        self.date_filter.setText("Select Date")
        self.apply_filter()

    def show_my_bookings(self):
        self.my_bookings_window = MyBookingsWindow(self.frequentFlyer, self)
        self.my_bookings_window.populate_bookings()
        self.my_bookings_window.show()

    def create_bottom_bar(self):
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                color: #ECF0F1;
            }
        """)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(20, 10, 20, 10)
        
        footer_text = QLabel("Version 1.0.3   |   © 2024 Israel Flight   |   support@israelflight.com   |   Tel: +972-3-1234567   |   Terms of Service   |   Privacy Policy   ")
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setStyleSheet("""
            color: #FFFFFF;
            font-size: 13px;
            font-weight: bold
        """)
        bottom_layout.addWidget(footer_text)

        return bottom_bar

    def go_to_home_screen(self):
        self.login_screen.show()
        self.close()

    def show_flight_details(self, flight):
     details_dialog = QDialog(self)
     details_dialog.setWindowTitle(f"Flight Details - {flight.FlightId}")
     details_dialog.setFixedSize(450, 500)
     details_dialog.setStyleSheet("""
        QDialog {
            background-color: #F0F4F8;
        }
        QLabel {
            font-size: 14px;
            color: #004aad;
            background: transparent;
        }
        QLabel#header {
            font-size: 24px;
            color: #004aad;
            font-weight: bold;
            background: transparent;
        }
        QWidget#header_widget {
            background: transparent;
        }
    """)

     main_layout = QVBoxLayout(details_dialog)
     main_layout.setSpacing(20)
     main_layout.setContentsMargins(20, 20, 20, 20)

    # Header (with explicit transparency)
     header_widget = QWidget()
     header_widget.setObjectName("header_widget")
     header_layout = QHBoxLayout(header_widget)
     header_layout.setContentsMargins(0, 0, 0, 0)
     header_layout.setSpacing(10)

     icon_label = QLabel()
     icon_label.setPixmap(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\details_icon.png").pixmap(QSize(40, 40)))
     icon_label.setStyleSheet("background: transparent;")
    
     header_label = QLabel("Flight Details")
     header_label.setObjectName("header")
    
     header_layout.addWidget(icon_label)
     header_layout.addWidget(header_label)
     header_layout.addStretch()
 
     main_layout.addWidget(header_widget)

    # Separator (optional, you can remove if not needed)
     separator = QFrame()
     separator.setFrameShape(QFrame.HLine)
     separator.setStyleSheet("background-color: #4A90E2;")
     main_layout.addWidget(separator)
 
     # Details
     details_widget = QWidget()
     details_layout = QVBoxLayout(details_widget)
     details_layout.setSpacing(10)

     details = [
        ("Flight ID", flight.FlightId),
        ("Plane ID", flight.PlaneId),
        ("Departure", flight.DepartureLocation),
        ("Arrival", flight.LandingLocation),
        ("Departure Time", flight.DepartureDateTime.strftime('%Y-%m-%d %H:%M')),
        ("Estimated Arrival", flight.EstimatedLandingDateTime.strftime('%Y-%m-%d %H:%M')),
        ("Price", f"${flight.FlightPrice:.2f}")
    ]

     for label, value in details:
        row_layout = QHBoxLayout()
        label_widget = QLabel(f"<b>{label}:</b>")
        label_widget.setFixedWidth(150)
        value_widget = QLabel(str(value))
        value_widget.setWordWrap(True)
        row_layout.addWidget(label_widget)
        row_layout.addWidget(value_widget)
        details_layout.addLayout(row_layout)

     scroll_area = QScrollArea()
     scroll_area.setWidgetResizable(True)
     scroll_area.setWidget(details_widget)
     scroll_area.setStyleSheet("background-color: white; border-radius: 10px;")
     main_layout.addWidget(scroll_area)

     # Book Button
     book_button = QPushButton(" Book Flight")
     book_button.setStyleSheet("""
        QPushButton {
            background-color: #004aad ;
            color: white;
            padding: 12px;
            border: none;
            border-radius:  10px;
            font-size: 20px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #3A80D2;
        }
    """)
     book_button.setIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\book_icon.png"))
     book_button.setIconSize(QSize(40, 40))
     book_button.clicked.connect(lambda: self.book_flight(flight, details_dialog))
     main_layout.addWidget(book_button)

     details_dialog.exec()

    def book_flight(self, flight, dialog):
        if HebcalController.check_flight_during_shabbat(flight.EstimatedLandingDateTime):
            error_dialog = QMessageBox(self)
            error_dialog.setWindowTitle("Booking Error")
            error_dialog.setText("The landing time falls on Shabbat, so you cannot book this flight.")
            error_dialog.setIcon(QMessageBox.Warning)
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec()
            dialog.accept()
            return

        booking = Booking(
            bookingId=israel_flight_instance.Bookings[-1].bookingId + 1,
            flightId=flight.FlightId,
            frequentFlyerId=self.frequentFlyer.frequentFlyerID,
            bookingDate=datetime.now(),
            ticketId=f"TICKET{self.frequentFlyer.frequentFlyerID}_{random.randint(1000, 9999)}",
            flightPrice=flight.FlightPrice,
        )

        BookingController.add_booking(booking.to_json())
        israel_flight_instance.Bookings = [Booking.from_json(booking_data) for booking_data in BookingController.get_bookings()]

        success_dialog = QMessageBox(self)
        success_dialog.setWindowTitle("Booking Confirmed")
        success_dialog.setText("Your flight has been booked successfully!")
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setStandardButtons(QMessageBox.Ok)
        success_dialog.exec()
        dialog.accept()