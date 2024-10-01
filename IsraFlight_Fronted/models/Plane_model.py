from typing import Optional, Dict, Any

class Plane:
    """
    Represents a plane in the system.
    """

    def __init__(self, planeId: int, manufacturer: str, model: str, yearOfManufacture: int,
                 nickname: Optional[str] = None, imageUrl: Optional[str] = None):
        """
        Initialize a Plane object.

        Args:
            planeId (int): The unique identifier for the plane.
            manufacturer (str): The manufacturer of the plane.
            model (str): The model of the plane.
            yearOfManufacture (int): The year the plane was manufactured.
            nickname (Optional[str]): The nickname of the plane, if any.
            imageUrl (Optional[str]): The URL of the plane's image, if any.
        """
        self.planeId = planeId
        self.manufacturer = manufacturer
        self.model = model
        self.yearOfManufacture = yearOfManufacture
        self.nickname = nickname
        self.imageUrl = imageUrl
    
    def __repr__(self):
        """
        Return a string representation of the Plane object.

        Returns:
            str: A string representation of the Plane object.
        """
        return (f"Plane(planeId={self.planeId}, manufacturer={self.manufacturer}, "
                f"model={self.model}, yearOfManufacture={self.yearOfManufacture}, "
                f"nickname={self.nickname}, imageUrl={self.imageUrl})")

    def update_details(self, manufacturer: Optional[str] = None, model: Optional[str] = None,
                      nickname: Optional[str] = None, yearOfManufacture: Optional[int] = None,
                      imageUrl: Optional[str] = None):
        """
        Update the details of the plane.

        Args:
            manufacturer (Optional[str]): New manufacturer if provided.
            model (Optional[str]): New model if provided.
            nickname (Optional[str]): New nickname if provided.
            yearOfManufacture (Optional[int]): New year of manufacture if provided.
            imageUrl (Optional[str]): New image URL if provided.
        """
        if manufacturer is not None:
            self.manufacturer = manufacturer
        if model is not None:
            self.model = model
        if nickname is not None:
            self.nickname = nickname
        if yearOfManufacture is not None:
            self.yearOfManufacture = yearOfManufacture
        if imageUrl is not None:
            self.imageUrl = imageUrl
    
    def to_json(plane) -> Dict[str, Any]:
        """
        Convert a Plane object to a dictionary (e.g., for sending to an API).

        Returns:
            Dict[str, Any]: A dictionary representation of the Plane object.
        """
        return {
            'planeID': plane.planeId,
            'manufacturer': plane.manufacturer,
            'model': plane.model,
            'yearOfManufacture': plane.yearOfManufacture,
            'nickname': plane.nickname,
            'imageURL': plane.imageUrl
        }
    
    @classmethod
    def from_json(cls, jsonData: Dict[str, Any]) -> 'Plane':
        """
        Create a Plane object from JSON data.

        Args:
            jsonData (Dict[str, Any]): JSON data representing a plane.

        Returns:
            Plane: A Plane object created from the JSON data.
        """
        return cls(
            planeId=jsonData.get('planeID', 'N/A'),
            manufacturer=jsonData.get('manufacturer', 'N/A'),
            model=jsonData.get('model', 'N/A'),
            yearOfManufacture=jsonData.get('yearOfManufacture', 'N/A'),
            nickname=jsonData.get('nickname', 'N/A'),
            imageUrl=jsonData.get('imageURL', 'N/A')
        )