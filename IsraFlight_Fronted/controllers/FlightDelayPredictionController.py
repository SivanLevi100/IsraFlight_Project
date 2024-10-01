import requests
from datetime import datetime, timedelta
import json

class FlightDelayPredictionController:
    def __init__(self, base_url="http://localhost:8000"):
        """
        Initialize the FlightDelayPredictionController.
        
        Args:
            base_url (str): The base URL for the prediction API.
        """
        self.base_url = base_url
        self.predict_endpoint = f"{self.base_url}/predict"

    def predict_delay(self, flight_data):
        """
        Predict flight delay based on given flight data.
        
        Args:
            flight_data (dict): The data of the flight for prediction.
        
        Returns:
            dict: Prediction results if successful, None otherwise.
        """
        try:
            response = requests.post(self.predict_endpoint, json=flight_data)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            print(response.json())  # Debug print
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def format_flight_data(self, occupancy, plane_nickname, departure_hour, day_of_week, departure_location):
        """
        Format flight data for prediction.
        
        Args:
            occupancy (str): The occupancy status of the flight.
            plane_nickname (str): The nickname of the plane.
            departure_hour (int): The hour of departure.
            day_of_week (int): The day of the week (1-7).
            departure_location (str): The departure location code.
        
        Returns:
            dict: Formatted flight data for prediction.
        """
        return {
            "Occupancy": occupancy,
            "PlaneNickname": plane_nickname,
            "DepartureHour": departure_hour,
            "DayOfWeek": day_of_week,
            "DepartureLocation": departure_location
        }

    def print_prediction_result(self, prediction):
        """
        Print the prediction result.
        
        Args:
            prediction (dict): The prediction result to print.
        """
        if prediction:
            print(f"Delay Prediction: {prediction['delay_prediction']}")
            print(f"Delay Probability: {prediction['delay_probability']}%")
        else:
            print("Unable to get prediction.")

# Example usage
if __name__ == "__main__":
    controller = FlightDelayPredictionController()

    # Example flight data
    flight_data = controller.format_flight_data(
        occupancy="full",
        plane_nickname="Plane A",
        departure_hour=14,
        day_of_week=3,  # Wednesday
        departure_location="TLV"
    )

    prediction = controller.predict_delay(flight_data)
    controller.print_prediction_result(prediction)

    departure_datetime = datetime(2024, 9, 22, 15, 30, 45)  # 22/09/2024 15:30:45
    print(departure_datetime.hour)