from typing import Dict, Any, Optional
from datetime import datetime

class FrequentFlyer:
    """
    Represents a frequent flyer in the system.
    """

    def __init__(self, frequentFlyerID: int, username: str, passwordHash: str, email: str,
                 firstName: str, lastName: str, passportNumber: str, dateOfBirth: datetime):
        """
        Initialize a FrequentFlyer object.

        Args:
            frequentFlyerID (int): The unique identifier for the frequent flyer.
            username (str): The username of the frequent flyer.
            passwordHash (str): The hashed password of the frequent flyer.
            email (str): The email address of the frequent flyer.
            firstName (str): The first name of the frequent flyer.
            lastName (str): The last name of the frequent flyer.
            passportNumber (str): The passport number of the frequent flyer.
            dateOfBirth (datetime): The date of birth of the frequent flyer.
        """
        self.frequentFlyerID = frequentFlyerID
        self.username = username
        self.passwordHash = passwordHash
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.passportNumber = passportNumber
        self.dateOfBirth = dateOfBirth

    def update_details(self, username: Optional[str] = None, passwordHash: Optional[str] = None,
                      email: Optional[str] = None, firstName: Optional[str] = None,
                      lastName: Optional[str] = None, passportNumber: Optional[str] = None,
                      dateOfBirth: Optional[datetime] = None):
        """
        Update the details of the frequent flyer.

        Args:
            username (Optional[str]): New username if provided.
            passwordHash (Optional[str]): New password hash if provided.
            email (Optional[str]): New email if provided.
            firstName (Optional[str]): New first name if provided.
            lastName (Optional[str]): New last name if provided.
            passportNumber (Optional[str]): New passport number if provided.
            dateOfBirth (Optional[datetime]): New date of birth if provided.
        """
        if username is not None:
            self.username = username
        if passwordHash is not None:
            self.passwordHash = passwordHash
        if email is not None:
            self.email = email
        if firstName is not None:
            self.firstName = firstName
        if lastName is not None:
            self.lastName = lastName
        if passportNumber is not None:
            self.passportNumber = passportNumber
        if dateOfBirth is not None:
            self.dateOfBirth = dateOfBirth

    @classmethod
    def from_json(cls, jsonData: Dict[str, Any]) -> 'FrequentFlyer':
        """
        Create a FrequentFlyer object from JSON data.

        Args:
            jsonData (Dict[str, Any]): JSON data representing a frequent flyer.

        Returns:
            FrequentFlyer: A FrequentFlyer object created from the JSON data.
        """
        return cls(
            frequentFlyerID=jsonData.get('frequentFlyerID', 0),
            username=jsonData.get('username', 'N/A'),
            passwordHash=jsonData.get('passwordHash', 'N/A'),
            email=jsonData.get('email', 'N/A'),
            firstName=jsonData.get('firstName', 'N/A'),
            lastName=jsonData.get('lastName', 'N/A'),
            passportNumber=jsonData.get('passportNumber', 'N/A'),
            dateOfBirth=datetime.fromisoformat(jsonData.get('dateOfBirth', '1900-01-01T00:00:00'))
        )

    def to_json(self) -> Dict[str, Any]:
        """
        Convert a FrequentFlyer object to a dictionary (e.g., for sending to an API).

        Returns:
            Dict[str, Any]: A dictionary representation of the FrequentFlyer object.
        """
        return {
            'frequentFlyerID': self.frequentFlyerID,
            'username': self.username,
            'passwordHash': self.passwordHash,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'passportNumber': self.passportNumber,
            'dateOfBirth': self.dateOfBirth.strftime('%Y-%m-%dT%H:%M:%S')
        }

    def __repr__(self):
        """
        Return a string representation of the FrequentFlyer object.

        Returns:
            str: A string representation of the FrequentFlyer object.
        """
        return (f"FrequentFlyer(frequentFlyerID={self.frequentFlyerID}, username='{self.username}', "
                f"passwordHash='{self.passwordHash}', email='{self.email}', firstName='{self.firstName}', "
                f"lastName='{self.lastName}', passportNumber='{self.passportNumber}', "
                f"dateOfBirth={self.dateOfBirth})")