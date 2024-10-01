from typing import Dict, Any, Optional

class Airport:
    """
    Represents an airport in the system.
    """

    def __init__(self, airportId: int, name: str, location: str, iata: str):
        """
        Initialize an Airport object.

        Args:
            airportId (int): The unique identifier for the airport.
            name (str): The name of the airport.
            location (str): The location of the airport.
            iata (str): The IATA code of the airport.
        """
        self.airportId = airportId
        self.name = name
        self.location = location
        self.iata = iata

    def update_details(self, name: Optional[str] = None, location: Optional[str] = None, 
                      iata: Optional[str] = None):
        """
        Update the details of the airport.

        Args:
            name (Optional[str]): New name if provided.
            location (Optional[str]): New location if provided.
            iata (Optional[str]): New IATA code if provided.
        """
        if name is not None:
            self.name = name
        if location is not None:
            self.location = location
        if iata is not None:
            self.iata = iata

    @classmethod
    def from_json(cls, jsonData: Dict[str, Any]) -> 'Airport':
        """
        Create an Airport object from JSON data.

        Args:
            jsonData (Dict[str, Any]): JSON data representing an airport.

        Returns:
            Airport: An Airport object created from the JSON data.
        """
        return cls(
            airportId=jsonData.get('airportId', 0),
            name=jsonData.get('name', 'N/A'),
            location=jsonData.get('location', 'N/A'),
            iata=jsonData.get('iata', 'N/A')
        )

    def to_json(self) -> Dict[str, Any]:
        """
        Convert an Airport object to a dictionary (e.g., for sending to an API).

        Returns:
            Dict[str, Any]: A dictionary representation of the Airport object.
        """
        return {
            'airportId': self.airportId,
            'name': self.name,
            'location': self.location,
            'iata': self.iata
        }

    def __repr__(self):
        """
        Return a string representation of the Airport object.

        Returns:
            str: A string representation of the Airport object.
        """
        return (f"Airport(airportId={self.airportId}, name='{self.name}', "
                f"location='{self.location}', iata='{self.iata}')")