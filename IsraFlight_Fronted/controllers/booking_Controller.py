import requests
from datetime import datetime

class BookingController:
    BASE_URL = "https://localhost:7292/api/Booking"  # Base URL of the API

    @staticmethod
    def get_bookings():
        """
        Retrieve a list of all bookings.
        
        Returns:
            JSON: List of bookings if successful, error message otherwise.
        """
        try:
            response = requests.get(BookingController.BASE_URL, verify=False)
            response.raise_for_status()  # Check for HTTP errors
            return response.json()  # Return the list of bookings
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def get_booking_by_id(booking_id):
        """
        Retrieve a specific booking by its ID.
        
        Args:
            booking_id (int): The ID of the booking to retrieve.
        
        Returns:
            JSON: Booking details if successful, error message otherwise.
        """
        try:
            url = f"{BookingController.BASE_URL}/{booking_id}"
            response = requests.get(url, verify=False)
            response.raise_for_status()
            return response.json()  # Return the booking details
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def add_booking(booking_data):
        """
        Add a new booking.
        
        Args:
            booking_data (dict): The data of the booking to be added.
        
        Returns:
            JSON: Added booking details if successful, error message otherwise.
        """
        try:
            response = requests.post(BookingController.BASE_URL, json=booking_data, verify=False)
            response.raise_for_status()  # Raises an exception for HTTP errors
            print(f"Booking added successfully: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to add booking: {e}")
            if e.response:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response content: {e.response.text}")
            return f"Error: {e}"

    @staticmethod
    def update_booking(booking_id, booking_data):
        """
        Update an existing booking by its ID.
        
        Args:
            booking_id (int): The ID of the booking to update.
            booking_data (dict): The updated booking data.
        
        Returns:
            str: Success message if update is successful, error message otherwise.
        """
        try:
            url = f"{BookingController.BASE_URL}/{booking_id}"
            response = requests.put(url, json=booking_data, verify=False)
            response.raise_for_status()
            return "Booking updated successfully"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def delete_booking(booking_id):
        """
        Delete a booking by its ID.
        
        Args:
            booking_id (int): The ID of the booking to delete.
        
        Returns:
            str: Success message if deletion is successful, error message otherwise.
        """
        try:
            url = f"{BookingController.BASE_URL}/{booking_id}"
            response = requests.delete(url, verify=False)
            response.raise_for_status()
            return "Booking deleted successfully"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"