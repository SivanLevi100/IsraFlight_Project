from datetime import datetime
from typing import Optional, Dict, Any

class Ticket:
    """
    Represents a ticket in the system.
    """

    def __init__(self, ticketId: str, bookingId: int, flightId: str, departureLocation: str,
                 landingLocation: str, departureDatetime: datetime, estimatedLandingDatetime: datetime,
                 ticketUrl: str):
        """
        Initialize a Ticket object.

        Args:
            ticketId (str): The unique identifier for the ticket.
            bookingId (int): The ID of the associated booking.
            flightId (str): The ID of the associated flight.
            departureLocation (str): The departure location.
            landingLocation (str): The landing location.
            departureDatetime (datetime): The departure date and time.
            estimatedLandingDatetime (datetime): The estimated landing date and time.
            ticketUrl (str): The URL of the ticket.
        """
        self.ticketId = ticketId
        self.bookingId = bookingId
        self.flightId = flightId
        self.departureLocation = departureLocation
        self.landingLocation = landingLocation
        self.departureDatetime = departureDatetime
        self.estimatedLandingDatetime = estimatedLandingDatetime
        self.ticketUrl = ticketUrl
        
    def update_details(self, departureLocation: Optional[str] = None, landingLocation: Optional[str] = None,
                      departureDatetime: Optional[datetime] = None, estimatedLandingDatetime: Optional[datetime] = None,
                      ticketUrl: Optional[str] = None):
        """
        Update the details of the ticket.

        Args:
            departureLocation (Optional[str]): New departure location if provided.
            landingLocation (Optional[str]): New landing location if provided.
            departureDatetime (Optional[datetime]): New departure date and time if provided.
            estimatedLandingDatetime (Optional[datetime]): New estimated landing date and time if provided.
            ticketUrl (Optional[str]): New ticket URL if provided.
        """
        if departureLocation is not None:
            self.departureLocation = departureLocation
        if landingLocation is not None:
            self.landingLocation = landingLocation
        if departureDatetime is not None:
            self.departureDatetime = departureDatetime
        if estimatedLandingDatetime is not None:
            self.estimatedLandingDatetime = estimatedLandingDatetime
        if ticketUrl is not None:
            self.ticketUrl = ticketUrl

   
    @classmethod
    def from_json(cls, jsonData: Dict[str, Any]) -> 'Ticket':
         """
        Create a Ticket object from JSON data.

        Args:
            jsonData (Dict[str, Any]): JSON data representing a ticket.

        Returns:
            Ticket: A Ticket object created from the JSON data.
        """
         return cls(
            ticketId=jsonData.get('ticketId', 'N/A'),
            bookingId=jsonData.get('bookingId', 0),
            flightId=jsonData.get('flightId', 'N/A'),
            departureLocation=jsonData.get('departureLocation', 'N/A'),
            landingLocation=jsonData.get('landingLocation', 'N/A'),
            departureDatetime=datetime.fromisoformat(jsonData.get('departureDatetime', '1900-01-01T00:00:00')),
            estimatedLandingDatetime=datetime.fromisoformat(jsonData.get('estimatedLandingDatetime', '1900-01-01T00:00:00')),
            ticketUrl=jsonData.get('ticketUrl', 'N/A'),
            
        )

    def to_json(self) -> Dict[str, Any]:
        # Convert a Ticket object to a dictionary (e.g., for sending to an API)
        return {
            'ticketId': self.ticketId,
            'bookingId': self.bookingId,
            'flightId': self.flightId,
            'departureLocation': self.departureLocation,
            'landingLocation': self.landingLocation,
            'departureDatetime': self.departureDatetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'estimatedLandingDatetime': self.estimatedLandingDatetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'ticketUrl': self.ticketUrl,
            
        }

    def __repr__(self):
        return (f"Ticket(ticketId='{self.ticketId}', bookingId={self.bookingId}, "
                f"flightId='{self.flightId}', departureLocation='{self.departureLocation}', "
                f"landingLocation='{self.landingLocation}', departureDatetime={self.departureDatetime}, "
                f"estimatedLandingDatetime={self.estimatedLandingDatetime}, ticketUrl='{self.ticketUrl}'")