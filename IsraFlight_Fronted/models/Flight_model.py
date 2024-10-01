from typing import Optional, Dict, Any
from datetime import datetime

class Flight:
    """
    Represents a flight in the system.
    """

    def __init__(self, FlightId: int, PlaneId: int, DepartureLocation: str, LandingLocation: str,
                 DepartureDateTime: datetime, EstimatedLandingDateTime: datetime,
                 FlightPrice: float):
        """
        Initialize a Flight object.

        Args:
            FlightId (int): The unique identifier for the flight.
            PlaneId (int): The ID of the associated plane.
            DepartureLocation (str): The departure location of the flight.
            LandingLocation (str): The landing location of the flight.
            DepartureDateTime (datetime): The departure date and time.
            EstimatedLandingDateTime (datetime): The estimated landing date and time.
            FlightPrice (float): The price of the flight.
        """
        self.FlightId = FlightId
        self.PlaneId = PlaneId
        self.DepartureLocation = DepartureLocation
        self.LandingLocation = LandingLocation
        self.DepartureDateTime = DepartureDateTime
        self.EstimatedLandingDateTime = EstimatedLandingDateTime
        self.FlightPrice = FlightPrice

    def update_details(self, departureLocation: Optional[str] = None, landingLocation: Optional[str] = None,
                      departureDateTime: Optional[datetime] = None, 
                      estimatedLandingDateTime: Optional[datetime] = None, 
                      flightPrice: Optional[float] = None, plane=None):
        """
        Update the details of the flight.

        Args:
            departureLocation (Optional[str]): New departure location if provided.
            landingLocation (Optional[str]): New landing location if provided.
            departureDateTime (Optional[datetime]): New departure date and time if provided.
            estimatedLandingDateTime (Optional[datetime]): New estimated landing date and time if provided.
            flightPrice (Optional[float]): New flight price if provided.
            plane (Optional): New associated plane object if provided.
        """
        if departureLocation is not None:
            self.DepartureLocation = departureLocation
        if landingLocation is not None:
            self.LandingLocation = landingLocation
        if departureDateTime is not None:
            self.DepartureDateTime = departureDateTime
        if estimatedLandingDateTime is not None:
            self.EstimatedLandingDateTime = estimatedLandingDateTime
        if flightPrice is not None:
            self.FlightPrice = flightPrice

    @classmethod
    def from_json(cls, jsonData: Dict[str, Any]) -> 'Flight':
        """
        Create a Flight object from JSON data.

        Args:
            jsonData (Dict[str, Any]): JSON data representing a flight.

        Returns:
            Flight: A Flight object created from the JSON data.
        """
        return cls(
            FlightId=jsonData.get('flightID', 'N/A'),
            PlaneId=jsonData.get('planeID', 'N/A'),
            DepartureLocation=jsonData.get('departureLocation', 'N/A'),
            LandingLocation=jsonData.get('landingLocation', 'N/A'),
            DepartureDateTime=datetime.fromisoformat(jsonData.get('departureDateTime', 'N/A')),
            EstimatedLandingDateTime=datetime.fromisoformat(jsonData.get('estimatedLandingDateTime', 'N/A')),
            FlightPrice=jsonData.get('flightPrice', 'N/A'),
        )

    def to_json(self) -> Dict[str, Any]:
        """
        Convert a Flight object to a dictionary (e.g., for sending to an API).

        Returns:
            Dict[str, Any]: A dictionary representation of the Flight object.
        """
        return {
            'flightID': self.FlightId,
            'planeID': self.PlaneId,
            'departureLocation': self.DepartureLocation,
            'landingLocation': self.LandingLocation,
            'departureDateTime': self.DepartureDateTime.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'estimatedLandingDateTime': self.EstimatedLandingDateTime.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'flightPrice': self.FlightPrice,
        }

    def __repr__(self):
        """
        Return a string representation of the Flight object.

        Returns:
            str: A string representation of the Flight object.
        """
        return (f"Flight(flightId={self.FlightId}, planeId={self.PlaneId}, "
            f"departureLocation='{self.DepartureLocation}', landingLocation='{self.LandingLocation}', "
            f"departureDateTime={self.DepartureDateTime}, "
            f"estimatedLandingDateTime={self.EstimatedLandingDateTime}, "
            f"flightPrice={self.FlightPrice})")