import json
from plane_controller import PlaneController
from flight_controller import FlightController

def main():
    """
    Main function to retrieve and display plane and flight data.
    """
    # Retrieve the list of planes
    planes_data = PlaneController.get_planes()
    
    # Retrieve the list of flights
    flights_data = FlightController.get_flights()
    
    # Check if there's an error in the planes response
    if isinstance(planes_data, str) and planes_data.startswith("Error"):
        print(planes_data)
    else:
        # If the response is a list of objects (dictionaries), print all plane details
        print("Planes data:")
        for plane in planes_data:
            print(json.dumps(plane, indent=4))  # Print the information in a formatted JSON format

    # Check if there's an error in the flights response
    if isinstance(flights_data, str) and flights_data.startswith("Error"):
        print(flights_data)
    else:
        # If the response is a list of objects (dictionaries), print all flight details
        print("Flights data:")
        for flight in flights_data:
            print(json.dumps(flight, indent=4))  # Print the information in a formatted JSON format

if __name__ == "__main__":
    print("Starting main check...")
    main()