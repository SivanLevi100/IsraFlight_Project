import requests

class FrequentFlyerController:
    BASE_URL = "https://localhost:7292/api/FrequentFlyer"

    @staticmethod
    def get_frequent_flyers():
        """
        Retrieve a list of all frequent flyers.
        
        Returns:
            JSON: List of frequent flyers if successful, error message otherwise.
        """
        try:
            response = requests.get(FrequentFlyerController.BASE_URL, verify=False)  # SSL verification disabled
            response.raise_for_status()  # Check for HTTP errors
            return response.json()  # Return the list of frequent flyers
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def get_frequent_flyer_by_id(frequent_flyer_id):
        """
        Retrieve a specific frequent flyer by their ID.
        
        Args:
            frequent_flyer_id (int): The ID of the frequent flyer to retrieve.
        
        Returns:
            JSON: Frequent flyer details if successful, error message otherwise.
        """
        try:
            url = f"{FrequentFlyerController.BASE_URL}/{frequent_flyer_id}"
            response = requests.get(url, verify=False)  # SSL verification disabled
            response.raise_for_status()
            return response.json()  # Return the frequent flyer details
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def add_frequent_flyer(frequent_flyer_data):
        """
        Add a new frequent flyer.
        
        Args:
            frequent_flyer_data (dict): The data of the frequent flyer to be added.
        
        Returns:
            JSON: Added frequent flyer details if successful, error message otherwise.
        """
        try:
            response = requests.post(FrequentFlyerController.BASE_URL, json=frequent_flyer_data, verify=False)  # SSL verification disabled
            response.raise_for_status()
            return response.json()  # Return the added frequent flyer
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def update_frequent_flyer(frequent_flyer_id, frequent_flyer_data):
        """
        Update an existing frequent flyer by their ID.
        
        Args:
            frequent_flyer_id (int): The ID of the frequent flyer to update.
            frequent_flyer_data (dict): The updated frequent flyer data.
        
        Returns:
            str: Success message if update is successful, error message otherwise.
        """
        try:
            url = f"{FrequentFlyerController.BASE_URL}/{frequent_flyer_id}"
            response = requests.put(url, json=frequent_flyer_data, verify=False)  # SSL verification disabled
            response.raise_for_status()
            return "Frequent flyer updated successfully"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    @staticmethod
    def delete_frequent_flyer(frequent_flyer_id):
        """
        Delete a frequent flyer by their ID.
        
        Args:
            frequent_flyer_id (int): The ID of the frequent flyer to delete.
        
        Returns:
            str: Success message if deletion is successful, error message otherwise.
        """
        try:
            url = f"{FrequentFlyerController.BASE_URL}/{frequent_flyer_id}"
            response = requests.delete(url, verify=False)  # SSL verification disabled
            response.raise_for_status()
            return "Frequent flyer deleted successfully"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"