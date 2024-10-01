from typing import Optional, Dict, Any

class Admin:
    """
    Represents an administrator in the system.
    """

    def __init__(self, adminId: int, username: str, password: str, email: str):
        """
        Initialize an Admin object.

        Args:
            adminId (int): The unique identifier for the admin.
            username (str): The admin's username.
            password (str): The admin's password.
            email (str): The admin's email address.
        """
        self.adminId = adminId
        self.username = username
        self.password = password
        self.email = email

    def update_details(self, username: Optional[str] = None, password: Optional[str] = None, 
                      email: Optional[str] = None):
        """
        Update the details of the admin.

        Args:
            username (Optional[str]): New username if provided.
            password (Optional[str]): New password if provided.
            email (Optional[str]): New email if provided.
        """
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        if email is not None:
            self.email = email

    @classmethod
    def from_json(cls, jsonData: Dict[str, Any]) -> 'Admin':
        """
        Create an Admin object from JSON data.

        Args:
            jsonData (Dict[str, Any]): JSON data representing an admin.

        Returns:
            Admin: An Admin object created from the JSON data.
        """
        return cls(
            adminId=jsonData.get('adminId', 0),
            username=jsonData.get('username', 'N/A'),
            password=jsonData.get('password', 'N/A'),
            email=jsonData.get('email', 'N/A')
        )

    def to_json(self) -> Dict[str, Any]:
        """
        Convert an Admin object to a dictionary (e.g., for sending to an API).

        Returns:
            Dict[str, Any]: A dictionary representation of the Admin object.
        """
        return {
            'adminId': self.adminId,
            'username': self.username,
            'password': self.password,
            'email': self.email
        }

    def __repr__(self):
        """
        Return a string representation of the Admin object.

        Returns:
            str: A string representation of the Admin object.
        """
        return (f"Admin(adminId={self.adminId}, username='{self.username}', "
                f"password='{self.password}', email='{self.email}')")