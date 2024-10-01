from PySide6.QtGui import QFont, QColor, QPalette
from views.Opening_view import OpeningScreen
from models.IsraelFlight_model import IsraelFlight

def main():
    """
    Main function to initialize and run the IsraelFlight application.
    """
    from PySide6.QtWidgets import QApplication
    import sys

    # Create the application instance
    app = QApplication(sys.argv)

    # Set a custom palette for the app background
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))  # Light gray background
    app.setPalette(palette)

    # Create and show the main window (Opening Screen)
    main_window = OpeningScreen()
    main_window.show()

    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    # Initialize the IsraelFlight model
    IsraelFlightApp = IsraelFlight()
    
    # Run the main function
    main()