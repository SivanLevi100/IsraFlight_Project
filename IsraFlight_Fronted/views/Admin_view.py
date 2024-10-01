from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
    QScrollArea,
)
from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtCore import Qt, QSize
from views.FlightListScreen_view import FlightListScreen
from views.PlaneListScreen_view import PlaneListScreen
from models.IsraelFlight_model import israel_flight_instance
from datetime import date, datetime, timedelta
from collections import Counter

# Main class for the admin dashboard
class AdminScreen(QWidget):
    def __init__(self, homeScreen):
        super().__init__()
        self.setWindowIcon(
            QIcon(r"IsraelFlight_Fronted_6419_6037\Images\logo_icon.png")
        )
        self.setWindowTitle("Israel Flight Admin Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        self.showMaximized()
        self.setStyleSheet(
            """
            QWidget {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #f0f8ff, stop:1 #e6f2ff);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #004aad;
                color: white;
                border: none;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 18px;
                width: 180px;
            }
            QPushButton:hover {
                background-color: #1873CC;
            }
            QLabel {
                color: #000000;
                font-size: 14px;
            }
            QFrame {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 10px;
                border: 1px solid rgba(221, 221, 221, 0.5);
            }
            QLabel.no-border {
            border: none;
            }
        """
        )
        self.homeScreen = homeScreen

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top bar
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)

        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(30, 30, 30, 30)

        # Main content
        main_content_layout = QHBoxLayout()

        # Navigation panel
        nav_panel = self.create_nav_panel()
        main_content_layout.addWidget(nav_panel, 1)

        # Dashboard overview
        dashboard_overview = self.create_dashboard_overview()
        main_content_layout.addWidget(dashboard_overview, 2)

        content_layout.addLayout(main_content_layout)

        # Wrap content in a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Bottom bar
        bottom_bar = self.create_bottom_bar()
        main_layout.addWidget(bottom_bar)

    # Create the top bar of the dashboard
    def create_top_bar(self):
        top_bar = QFrame()
        top_bar.setStyleSheet(
            """
        QFrame {
            background-color: #FFFFFF;
            border-bottom: 2px solid #2980B9;
        }
    """
        )
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 10, 20, 10)

        # Logo on the left
        logo_label = QLabel()
        logo_label.setPixmap(
            QIcon("IsraelFlight_Fronted_6419_6037\Images\IsraelFlight_logo.png").pixmap(
                QSize(150, 150)
            )
        )
        logo_label.setStyleSheet("border: None;")
        top_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        # Title in the center
        title_label = QLabel("Flight Management System")
        title_label.setStyleSheet(
            """
        font-size: 35px;
        font-weight: bold;
        color: #1873CC;
        border: None;
    """
        )
        title_label.setAlignment(Qt.AlignCenter)
        # Stretch factor of 1 to center it
        top_layout.addWidget(title_label, 1)

        # Home button on the right
        home_button = QPushButton()
        home_button.setIcon(
            QIcon("IsraelFlight_Fronted_6419_6037\Images\home_icon.png")
        )
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

    # Create the navigation panel
    def create_nav_panel(self):
        nav_frame = QFrame()
        nav_layout = QVBoxLayout(nav_frame)

        def create_nav_button(icon, text, description, on_click):
            button_layout = QVBoxLayout()
            icon_label = QLabel()
            icon_label.setPixmap(
                 QIcon(f"IsraelFlight_Fronted_6419_6037\Images\{icon}").pixmap(
                QSize(70, 70)
            ))
            icon_label.setStyleSheet(" border: none")     
            icon_label.setAlignment(Qt.AlignCenter)
            button_layout.addWidget(icon_label)
            
            button = QPushButton(text)
            button.clicked.connect(on_click)
            button_layout.addWidget(button)

            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setStyleSheet("font-size: 12px; color: #1873CC; border: none")
            button_layout.addWidget(desc_label)

            return button_layout

        nav_layout.addLayout(
            create_nav_button(
                "flight_blue_icon.png",
                "Manage Flights",
                "Control flight schedules and operations",
                self.show_flights_screen,
            )
        )
        nav_layout.addLayout(
            create_nav_button(
                "airplane_icon.png",
                "Manage Aircraft",
                "Oversee fleet and maintenance",
                self.show_planes_screen,
            )
        )
        nav_layout.addStretch()

        return nav_frame
   
    # Create the dashboard overview
    def create_dashboard_overview(self):
        overview_frame = QFrame()
        overview_layout = QVBoxLayout(overview_frame)

        title = QLabel("Dashboard Overview")
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: #004391; margin-bottom: 15px; border: none;"
        )
        overview_layout.addWidget(title)
        grid_layout = QGridLayout()
        stats = [
            ("Total Flights Landing in TLV this week", str(get_flights_landing_this_week(self))),
            ("Active Aircraft", str(len(israel_flight_instance.planes))),
            ("Amount of frequent flyers in the IsraFlight", str(len(israel_flight_instance.FrequentFlyers))),
            ("Most Popular Destination", str(count_most_popular_landing_destination(self))),
        ]
    
        for i, (label, value) in enumerate(stats):
            stat_frame = QFrame()
            stat_frame.setStyleSheet(
                """
               
                border-radius: 8px;
                padding: 10px;
                background-color: #DEEAFF;
            """
            )
            stat_layout = QVBoxLayout(stat_frame)
            stat_label = QLabel(label)
            stat_label.setStyleSheet(
                "font-size: 22px; font-weight: bold; color: #000000;border: none;"
            )
            stat_value = QLabel(value)
            stat_value.setStyleSheet(
                "font-size: 30px; font-weight: bold; color: #006DEC; border: none; "
            )
            
            stat_value.setAlignment(Qt.AlignCenter)
            stat_label.setAlignment(Qt.AlignCenter)
            stat_layout.addWidget(stat_label)
            stat_layout.addWidget(stat_value)
            grid_layout.addWidget(stat_frame, i // 2, i % 2)

        overview_layout.addLayout(grid_layout)

        activities_label = QLabel("Recent Activities")
        activities_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; margin-top: 25px; margin-bottom: 10px; border: none;"
        )
        overview_layout.addWidget(activities_label)

        d = israel_flight_instance.Flights[-1].DepartureLocation
        e = israel_flight_instance.Flights[-1].LandingLocation
        m = israel_flight_instance.Flights[-1].DepartureDateTime.strftime("%H:%M:%S")
        activities_list = QLabel(
            f"• New flight added: {d} to {e} ({m})\n"
            "• Aircraft status updated: Maintenance completed (09:45)\n"
            "• Schedule change: Flight 302 delayed by 30 minutes (09:15)"
        )
        activities_list.setStyleSheet(
            """
            background-color: #DEEAFF;
            padding: 15px;
            border-radius: 5px;
            font-size: 14px;
            line-height: 1.6;
        """
        )
        overview_layout.addWidget(activities_list)

        return overview_frame

    # Create the bottom bar of the dashboard
    def create_bottom_bar(self):
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet(
            """
            QFrame {
                background-color: #34495E;
                border: none;
                border-radius: 0px;
                
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
            font-weight: bold
        """
        )
        bottom_layout.addWidget(footer_text)

        return bottom_bar

    # Navigate to the home screen
    def go_to_home_screen(self):
        self.homeScreen.show()
        self.close()

    # Show the flights management screen
    def show_flights_screen(self):
        self.flights_screen = FlightListScreen(self)
        self.flights_screen.show()
        self.close()

    # Show the planes management screen
    def show_planes_screen(self):
        self.planes_screen = PlaneListScreen(self)
        self.planes_screen.show()
        self.close()

# Get the number of flights landing in TLV this week
def get_flights_landing_this_week(self):
      this_week = []
      today = date.today()
    
      # If today is Sunday (0), keep it as the start date; otherwise, find the last Sunday
      start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    
      # Calculate the end of the week - Saturday
      end_of_week = start_of_week + timedelta(days=6)

      for flight in israel_flight_instance.Flights:
          if start_of_week <= flight.EstimatedLandingDateTime.date() <= end_of_week and flight.LandingLocation=="TLV":
              this_week.append(flight)
              print(flight.FlightId)

      return len(this_week) 
    
# Count the most popular landing destination
def count_most_popular_landing_destination(self):
    landing_destinations = []
    
    # Collect all landing destinations
    for flight in israel_flight_instance.Flights:
        # Ignore TLV
        if flight.LandingLocation != "TLV":
            landing_destinations.append(flight.LandingLocation)
    
    # Count occurrences of each landing destination
    destination_counts = Counter(landing_destinations)
    
    # Determine the most popular destination, if there are flights
    if destination_counts:
        most_common_destination, most_common_count = destination_counts.most_common(1)[0]
    else:
        most_common_destination, most_common_count = None, 0  # No flights to other destinations
    
    # Check if the most common destination is in the Airports list
    if most_common_destination:
        for airport in israel_flight_instance.Airports:
            if airport.iata == most_common_destination:
                return airport.location
    
    # If the destination is not found in the Airports list, return None
    return None