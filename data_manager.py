import requests
import os

SHEETY_ENDPOINT_PRICES = f"{os.environ.get("SHEETY_ENDPOINT")}/prices"
SHEETY_ENDPOINT_USERS = f"{os.environ.get("SHEETY_ENDPOINT")}/users"

HEADERS = {
    "Authorization": f"Bearer {os.environ.get("SHEETY_BEARER_TOKEN")}"
}


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.prices_data = []
        self.users_data = []

    def get_prices_data(self):
        """Returns a list with all the data found into Google Sheets prices sheet."""
        response = requests.get(url=SHEETY_ENDPOINT_PRICES, headers=HEADERS)
        json_data = response.json()

        self.prices_data = json_data["prices"]
        return self.prices_data

    def update_sheet_iata_code(self, iata_code, city_name):
        """Update a specific row from Google Sheets prices sheet, with a new iataCode"""
        id_row = [data_row['id'] for data_row in self.prices_data if data_row["city"] == city_name][0]

        update_body = {
            "price": {
                "iataCode": iata_code
            }
        }
        requests.put(url=f"{SHEETY_ENDPOINT_PRICES}/{id_row}", json=update_body, headers=HEADERS)

    def add_new_datarow(self, first_name, last_name, email):
        """Adds a new row with user data into Google Sheets users sheet"""
        body_row = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }
        requests.post(url=SHEETY_ENDPOINT_USERS, json=body_row, headers=HEADERS)

    def get_users_data(self):
        """Returns a list with all the data found into Google Sheets users sheet."""
        response = requests.get(url=SHEETY_ENDPOINT_USERS, headers=HEADERS)
        json_data = response.json()

        self.users_data = json_data["users"]

        return self.users_data
