import sys
import os
from models.Booking_model import Booking
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ast import Dict
from typing import Any
import requests 
from controllers.flight_controller import FlightController
from controllers.plane_controller import PlaneController
from controllers.FrequentFlyer_Controller import FrequentFlyerController
from models.Plane_model import Plane
from models.Flight_model import Flight
from models.FrequentFlyer_model import FrequentFlyer
from models.Airport_model import Airport
from controllers.booking_Controller import BookingController
from controllers.Airport_Controller import AirportController

class IsraelFlight:
    """
    Singleton class representing the IsraelFlight system.
    """
    _instance = None
    _is_initialized = False

    @classmethod
    def new(cls, *args, **kwargs):
        """
        Create a new instance of IsraelFlight if it doesn't exist.

        Raises:
            Exception: If an instance already exists.

        Returns:
            IsraelFlight: The singleton instance of IsraelFlight.
        """
        if cls._instance is not None:
            raise Exception("Cannot create another instance of IsraelFlight")
        cls._instance = super(IsraelFlight, cls).__new__(cls)
        cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(self):
        """
        Initialize the IsraelFlight instance with data from various controllers.
        """
        if not self._is_initialized:
            self.planes = [Plane.from_json(plane_data) for plane_data in PlaneController.get_planes()]
            self.Admins = None
            self.Flights = [Flight.from_json(flight_data) for flight_data in FlightController.get_flights()]
            self.Airports = [Airport.from_json(airport_data) for airport_data in AirportController.get_airports()]
            self.Bookings = [Booking.from_json(Booking_data) for Booking_data in BookingController.get_bookings()]
            self.FrequentFlyers = [FrequentFlyer.from_json(FrequentFlyer_data) for FrequentFlyer_data in FrequentFlyerController.get_frequent_flyers()]
            self.Tikets = None
            self._is_initialized = True

    def check_initialization_and_print_planes(self):
        """
        Check if the IsraelFlight instance is initialized and print the planes list.
        """
        if self._is_initialized:
            print("IsraelFlight_class is initialized.")
            print("Planes list:")
            for plane in self.planes:
                print(plane)  # Modify this line if you want to format the plane details differently
        else:
            print("IsraelFlight_class is not initialized.")

# Example usage:
# Initialize the singleton instance
if IsraelFlight._instance is None:
    israel_flight_instance = IsraelFlight.new()
    israel_flight_instance.check_initialization_and_print_planes()
else:
    print("Instance already exists.")