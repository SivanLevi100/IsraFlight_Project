import requests

class AirportController:
    BASE_URL = "https://localhost:7292/api/Airport"  # Base URL for the Airport API

    @staticmethod
    def get_airports():
        """
        Retrieve the list of airports.
        
        Returns:
            JSON: List of airports if successful, error message otherwise.
        """
        try:
            response = requests.get(AirportController.BASE_URL, verify=False)
            response.raise_for_status()
            return response.json()  # Return the list of airports
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def get_airport_by_id(airport_id):
        """
        Retrieve an airport by ID.
        
        Args:
            airport_id (int): The ID of the airport to retrieve.
        
        Returns:
            JSON: Airport details if successful, error message otherwise.
        """
        try:
            url = f"{AirportController.BASE_URL}/{airport_id}"
            response = requests.get(url, verify=False)
            response.raise_for_status()
            return response.json()  # Return the airport details
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def add_airport(airport_data):
        """
        Add a new airport.
        
        Args:
            airport_data (dict): The data of the airport to be added.
        
        Returns:
            JSON: Added airport details if successful, error message otherwise.
        """
        try:
            response = requests.post(AirportController.BASE_URL, json=airport_data, verify=False)
            response.raise_for_status()
            print(f"Airport added successfully: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to add airport: {e}")
            if e.response:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response content: {e.response.text}")
            return f"Error: {e}"

    @staticmethod
    def update_airport(airport_id, airport_data):
        """
        Update airport details by ID.
        
        Args:
            airport_id (int): The ID of the airport to update.
            airport_data (dict): The updated airport data.
        
        Returns:
            str: Success message if update is successful, error message otherwise.
        """
        try:
            url = f"{AirportController.BASE_URL}/{airport_id}"
            response = requests.put(url, json=airport_data, verify=False)
            response.raise_for_status()
            return "Airport updated successfully"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def delete_airport(airport_id):
        """
        Delete an airport by ID.
        
        Args:
            airport_id (int): The ID of the airport to delete.
        
        Returns:
            str: Success message if deletion is successful, error message otherwise.
        """
        try:
            url = f"{AirportController.BASE_URL}/{airport_id}"
            response = requests.delete(url, verify=False)
            response.raise_for_status()
            return "Airport deleted successfully"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"