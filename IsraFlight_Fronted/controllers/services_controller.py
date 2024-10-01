import requests
from datetime import datetime

class ServicesController:
    BASE_URL = "https://localhost:7292/api"  # Base URL of the API

    @staticmethod
    def validate_image(image_url):
        """
        Validate an image using the Imagga API.
        
        Args:
            image_url (str): The URL of the image to validate.
        
        Returns:
            bool or str: True if the image is a plane, False if not, or an error message.
        """
        validate_image_url = f"{ServicesController.BASE_URL}/Imagga/recognize-image"
        data = image_url
        print("Entering VALIDATE_IMAGE function")
        try:
            response = requests.post(validate_image_url, json=data, verify=False)
            print(response)
            if response.status_code == 200:
                print(f"response.status_code == 200: {response.json()}")
                result = response.json()  # Get the result from the API in JSON format
                if result == True:
                    print("THE IMAGE IS A PLANE")
                    return True
                elif result == False:
                    print("THE IMAGE IS NOT A PLANE")
                    return False
                return "Unexpected result format"
            else:
                return f"Error: {response.status_code}, {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"

class HebcalController:
    BASE_URL = "https://localhost:7292/api/hebcal"  # Backend API address

    @staticmethod
    def get_parasha(date):
        """
        Get the Torah portion (parasha) for a given date.
        
        Args:
            date (datetime): The date to get the parasha for.
        
        Returns:
            str: The parasha name or an error message.
        """
        try:
            url = f"{HebcalController.BASE_URL}/parasha"
            params = {"date": date.strftime('%Y-%m-%dT%H:%M:%S')}
            response = requests.get(url, params=params, verify=False)
            if response.status_code == 200:
                return response.text  # Return the parasha result
            else:
                return f"Error: {response.status_code}, {response.text}"
        except ValueError:
            return "Invalid date format"
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"

    @staticmethod
    def check_flight_during_shabbat(date):
        """
        Check if a flight is during Shabbat based on the landing date.
        
        Args:
            date (datetime): The landing date and time to check.
        
        Returns:
            bool: True if the flight is during Shabbat, False otherwise.
        """
        try:
            print(f"The date is: {date}")
            url = f"{HebcalController.BASE_URL}/is-flight-during-shabbat"
            response = requests.get(url, json=date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), verify=False)
            print(f"The status: {response.status_code}")
            if response.status_code == 200:
                is_during_shabbat = response.json()
                return bool(is_during_shabbat)  # Ensure the output is True or False
            else:
                return False  # In case of any other error, return False by default
        except ValueError:
            return False  # Invalid date, return False
        except requests.exceptions.RequestException as e:
            return False  # Request failed, return False

    @staticmethod
    def get_shabbat_times(date):
        """
        Get Shabbat start and end times for a given date.
        
        Args:
            date (datetime): The date to get Shabbat times for.
        
        Returns:
            dict: A dictionary containing Shabbat times or an error message.
        """
        try:
            url = f"{HebcalController.BASE_URL}/shabbat-times"
            params = {"date": date.strftime('%Y-%m-%dT%H:%M:%S')}
            response = requests.get(url, params=params, verify=False)
            if response.status_code == 200:
                print(f"The time for Shabbat is: {response.json()}")
                return response.json()  # Return the Shabbat times
            else:
                return f"Error: {response.status_code}, {response.text}"
        except ValueError:
            return "Invalid date format"
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"

# Example usage (commented out):
# date = datetime(2024, 9, 27)
# result = HebcalController.get_shabbat_times(date)
# if result:
#     print(f"Candle lighting time: {result['candleLighting']}")
#     print(f"Havdalah time: {result['havdalah']}")