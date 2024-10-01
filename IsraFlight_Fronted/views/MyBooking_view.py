from PySide6.QtWidgets import QWidget,QFrame,QHeaderView, QVBoxLayout,QMessageBox, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
from PySide6.QtGui import QFont, QIcon,QPixmap
from PySide6.QtCore import Qt, QSize
from controllers.booking_Controller import BookingController
from models.FrequentFlyer_model import FrequentFlyer
from models.IsraelFlight_model import israel_flight_instance
from models.Ticket_model import Ticket
from services.pdf_service import create_ticket_pdf
from datetime import datetime

# Main class for displaying user bookings
class MyBookingsWindow(QWidget):
    def __init__(self, frequentFlyer, frequentFlyer_screen):
        super().__init__()
        self.frequentFlyer = frequentFlyer
        self.frequentFlyer_screen = frequentFlyer_screen
        self.setWindowIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\logo_icon.png"))
        self.setWindowTitle("My Bookings - IsraFlight")
        self.showMaximized()
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                font-family: Arial, sans-serif;
            }
        """)

        self.init_ui()

    # Initialize the user interface
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.create_top_bar())

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        name_label = QLabel(f"Your Bookings, {self.frequentFlyer.firstName} {self.frequentFlyer.lastName}")
        name_label.setFont(QFont("Arial", 24, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: #2C3E50; margin-bottom: 20px;")
        content_layout.addWidget(name_label)

        self.bookings_table = self.create_bookings_table()
        content_layout.addWidget(self.bookings_table)

        close_button = QPushButton("Close")
        close_button.setFont(QFont("Arial", 14))
        close_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: white;
                    color: #E74C3C;
                    border: 2px solid #E74C3C;
                    border-radius: 10px;
                    padding: 5px 10px;
                    font-weight: bold;
                   
                }}
                QPushButton:hover {{
                    background-color: #E74C3C;
                    color: white;
                }}
            """)
        close_button.clicked.connect(self.close)
        content_layout.addWidget(close_button, alignment=Qt.AlignRight)

        main_layout.addLayout(content_layout)
        main_layout.addWidget(self.create_bottom_bar())

        self.populate_bookings()

    # Create the top bar of the window
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
        top_layout.addWidget(logo_label,alignment=Qt.AlignLeft)

        return top_bar

    # Create the bottom bar of the window
    def create_bottom_bar(self):
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet("""
            QFrame {
                background-color: #34495E;
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
    
    # Create the table for displaying bookings
    def create_bookings_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Booking ID", "Flight ID", "Ticket ID", "Booking Date", "PDF"
        ])
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setStyleSheet("""
    QTableWidget {
        background-color: white;
        gridline-color: #D3D3D3;
        border: 1px solid #D3D3D3;
        border-radius: 5px;
    }
    QHeaderView::section {
        background-color: #3498DB;
        color: white;
        padding: 5px;
        border: 1px solid #2980B9;
        font-weight: bold;
        font-size: 20px;
    }
    QTableWidget::item {
        padding: 5px;
        text-align: center;
        font-weight: bold;
        font-size: 25px
    }
""")
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        return table

    # Populate the bookings table with data
    def populate_bookings(self):
        filtered_bookings = [booking for booking in israel_flight_instance.Bookings if booking.frequentFlyerId == self.frequentFlyer.frequentFlyerID]
        self.bookings_table.setRowCount(len(filtered_bookings))

        # Create a font for the table items
        item_font = QFont()
        item_font.setPointSize(10)
        item_font.setBold(True)

        for row, booking in enumerate(filtered_bookings):
            # Create and set items with centered text and larger, bold font
            for col, value in enumerate([
                str(booking.bookingId),
                str(booking.flightId),
                str(booking.ticketId),
                booking.bookingDate.strftime('%Y-%m-%d %H:%M:%S')
            ]):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(item_font)
                self.bookings_table.setItem(row, col, item)

            self.bookings_table.setRowHeight(row, 50)

            # Create a container widget for the PDF button
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignCenter)

            pdf_button = QPushButton()
            pdf_button.setIcon(QIcon("IsraelFlight_Fronted_6419_6037/Images/PDF.png"))
            pdf_button.setIconSize(QSize(24, 24))
            pdf_button.setFixedSize(40, 40)
            pdf_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                }
                QPushButton:hover {
                    background-color: #E8F6FF;
                    border-radius: 20px;
                }
            """)
            pdf_button.clicked.connect(lambda _, b=booking: self.generate_pdf(b))

            layout.addWidget(pdf_button)
            self.bookings_table.setCellWidget(row, 4, container)

        # Adjust column widths to content
        self.bookings_table.resizeColumnsToContents()

    # Generate PDF for a booking
    def generate_pdf(self, booking):
        flight_choice = next((flight for flight in israel_flight_instance.Flights if booking.flightId == flight.FlightId), None)

        ticket = Ticket(booking.ticketId, booking.bookingId, booking.flightId, flight_choice.DepartureLocation,
                        flight_choice.LandingLocation, flight_choice.DepartureDateTime, 
                        flight_choice.EstimatedLandingDateTime, "url")
        myFrequentFlyer = self.frequentFlyer
        file_path = f"IsraelFlight_Fronted_6419_6037/PDF_files/ticket_{booking.ticketId}.pdf"
        create_ticket_pdf(ticket, file_path, myFrequentFlyer)
        
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("PDF Created")
        msg_box.setWindowIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\PDF.png"))
        msg_box.setText(f"PDF created successfully and saved at: {file_path}")
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #F0F4F8;
            }
            QLabel {
                color: #2C3E50;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()