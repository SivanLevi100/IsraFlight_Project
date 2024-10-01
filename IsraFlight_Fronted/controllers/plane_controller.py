import requests

class PlaneController:
    BASE_URL = "https://localhost:7292/api/Plane"

    @staticmethod
    def get_planes():
        """
        Retrieve the list of planes.
        
        Returns:
            JSON: List of planes if successful, error message otherwise.
        """
        try:
            response = requests.get(PlaneController.BASE_URL, verify=False)  # SSL verification disabled
            response.raise_for_status()  # Check for HTTP errors
            return response.json()  # Return the list of planes
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def get_plane_by_id(plane_id):
        """
        Retrieve a plane by ID.
        
        Args:
            plane_id (int): The ID of the plane to retrieve.
        
        Returns:
            JSON: Plane details if successful, error message otherwise.
        """
        try:
            url = f"{PlaneController.BASE_URL}/{plane_id}"
            response = requests.get(url, verify=False)  # SSL verification disabled
            response.raise_for_status()
            return response.json()  # Return the plane details
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def add_plane(plane_data):
        """
        Add a new plane.
        
        Args:
            plane_data (dict): The data of the plane to be added.
        
        Returns:
            JSON: Added plane details if successful, error message otherwise.
        """
        try:
            response = requests.post(PlaneController.BASE_URL, json=plane_data, verify=False)  # SSL verification disabled
            response.raise_for_status()
            return response.json()  # Return the added plane
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def update_plane(plane_id, plane_data):
        """
        Update plane details by ID.
        
        Args:
            plane_id (int): The ID of the plane to update.
            plane_data (dict): The updated plane data.
        
        Returns:
            str: Success message if update is successful, error message otherwise.
        """
        try:
            url = f"{PlaneController.BASE_URL}/{plane_id}"
            response = requests.put(url, json=plane_data, verify=False)  # SSL verification disabled
            response.raise_for_status()
            return "Plane updated successfully"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def delete_plane(plane_id):
        """
        Delete a plane by ID.
        
        Args:
            plane_id (int): The ID of the plane to delete.
        
        Returns:
            str: Success message if deletion is successful, error message otherwise.
        """
        try:
            url = f"{PlaneController.BASE_URL}/{plane_id}"
            response = requests.delete(url, verify=False)  # SSL verification disabled
            response.raise_for_status()
            return "Plane deleted successfully"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"