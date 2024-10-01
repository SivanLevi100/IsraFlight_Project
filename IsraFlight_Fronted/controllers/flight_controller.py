import requests

class FlightController:
    BASE_URL = "https://localhost:7292/api/Flight"  # Base URL of the API

    @staticmethod
    def get_flights():
        """
        Retrieve a list of all flights.
        
        Returns:
            JSON: List of flights if successful, error message otherwise.
        """
        try:
            response = requests.get(FlightController.BASE_URL, verify=False)
            response.raise_for_status()  # Check for HTTP errors
            return response.json()  # Return the list of flights
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def get_flight_by_id(flight_id):
        """
        Retrieve a specific flight by its ID.
        
        Args:
            flight_id (int): The ID of the flight to retrieve.
        
        Returns:
            JSON: Flight details if successful, error message otherwise.
        """
        try:
            url = f"{FlightController.BASE_URL}/{flight_id}"
            response = requests.get(url, verify=False)
            response.raise_for_status()
            return response.json()  # Return the flight details
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def add_flight(flight_data):
        """
        Add a new flight.
        
        Args:
            flight_data (dict): The data of the flight to be added.
        
        Returns:
            JSON: Added flight details if successful, error message otherwise.
        """
        try:
            response = requests.post(FlightController.BASE_URL, json=flight_data, verify=False)
            response.raise_for_status()  # Raises an exception for HTTP errors
            print(f"Flight added successfully: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to add flight: {e}")
            if e.response:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response content: {e.response.text}")
            return f"Error: {e}"

    @staticmethod
    def update_flight(flight_id, flight_data):
        """
        Update an existing flight by its ID.
        
        Args:
            flight_id (int): The ID of the flight to update.
            flight_data (dict): The updated flight data.
        
        Returns:
            str: Success message if update is successful, error message otherwise.
        """
        try:
            url = f"{FlightController.BASE_URL}/{flight_id}"
            response = requests.put(url, json=flight_data, verify=False)
            response.raise_for_status()
            return "Flight updated successfully"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def delete_flight(flight_id):
        """
        Delete a flight by its ID.
        
        Args:
            flight_id (int): The ID of the flight to delete.
        
        Returns:
            str: Success message if deletion is successful, error message otherwise.
        """
        try:
            url = f"{FlightController.BASE_URL}/{flight_id}"
            response = requests.delete(url, verify=False)
            response.raise_for_status()
            return "Flight deleted successfully"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"