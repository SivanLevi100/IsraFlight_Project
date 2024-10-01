from datetime import datetime
from typing import Optional, Dict, Any

class Booking:
    """
    Represents a booking in the system.
    """

    def __init__(self, bookingId: int, flightId: int, frequentFlyerId: int, bookingDate: datetime,
                 ticketId: str, flightPrice: float, flight = None, frequentFlyer = None):
        """
        Initialize a Booking object.

        Args:
            bookingId (int): The unique identifier for the booking.
            flightId (int): The ID of the associated flight.
            frequentFlyerId (int): The ID of the associated frequent flyer.
            bookingDate (datetime): The date and time of the booking.
            ticketId (str): The ticket identifier.
            flightPrice (float): The price of the flight.
            flight (Optional): The associated flight object.
            frequentFlyer (Optional): The associated frequent flyer object.
        """
        self.bookingId = bookingId
        self.flightId = flightId
        self.frequentFlyerId = frequentFlyerId
        self.bookingDate = bookingDate
        self.ticketId = ticketId
        self.flightPrice = flightPrice
        self.flight = flight
        self.frequentFlyer = frequentFlyer

    def update_details(self, flightId: Optional[int] = None, frequentFlyerId: Optional[int] = None,
                      bookingDate: Optional[datetime] = None, ticketId: Optional[str] = None,
                      flightPrice: Optional[float] = None, flight = None, frequentFlyer = None):
        """
        Update the details of the booking.

        Args:
            flightId (Optional[int]): New flight ID if provided.
            frequentFlyerId (Optional[int]): New frequent flyer ID if provided.
            bookingDate (Optional[datetime]): New booking date if provided.
            ticketId (Optional[str]): New ticket ID if provided.
            flightPrice (Optional[float]): New flight price if provided.
            flight (Optional): New associated flight object if provided.
            frequentFlyer (Optional): New associated frequent flyer object if provided.
        """
        if flightId is not None:
            self.flightId = flightId
        if frequentFlyerId is not None:
            self.frequentFlyerId = frequentFlyerId
        if bookingDate is not None:
            self.bookingDate = bookingDate
        if ticketId is not None:
            self.ticketId = ticketId
        if flightPrice is not None:
            self.flightPrice = flightPrice
        if flight is not None:
            self.flight = flight
        if frequentFlyer is not None:
            self.frequentFlyer = frequentFlyer

    @classmethod
    def from_json(cls, jsonData: Dict[str, Any]) -> 'Booking':
        """
        Create a Booking object from JSON data.

        Args:
            jsonData (Dict[str, Any]): JSON data representing a booking.

        Returns:
            Booking: A Booking object created from the JSON data.
        """
        return cls(
            bookingId=jsonData.get('bookingID', 0),
            flightId=jsonData.get('flightID', 0),
            frequentFlyerId=jsonData.get('frequentFlyerID', 0),
            bookingDate=datetime.fromisoformat(jsonData.get('bookingDate', '1900-01-01T00:00:00')),
            ticketId=jsonData.get('ticketID', 'N/A'),
            flightPrice=jsonData.get('flightPrice', 0.0),
        )

    def to_json(self) -> Dict[str, Any]:
        """
        Convert a Booking object to a dictionary (e.g., for sending to an API).

        Returns:
            Dict[str, Any]: A dictionary representation of the Booking object.
        """
        return {
            'bookingID': self.bookingId,
            'flightID': self.flightId,
            'frequentFlyerID': self.frequentFlyerId,
            'bookingDate': self.bookingDate.strftime('%Y-%m-%dT%H:%M:%S'),
            'ticketID': self.ticketId,
            'flightPrice': self.flightPrice,
        }

    def __repr__(self):
        """
        Return a string representation of the Booking object.

        Returns:
            str: A string representation of the Booking object.
        """
        return (f"Booking(bookingId={self.bookingId}, flightId={self.flightId}, "
                f"frequentFlyerId={self.frequentFlyerId}, bookingDate={self.bookingDate}, "
                f"ticketId='{self.ticketId}', flightPrice={self.flightPrice})")