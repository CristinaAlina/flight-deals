import requests
import os

SHEETY_GET_ENDPOINT = os.environ.get("SHEETY_GET_ENDPOINT")

HEADERS = {
    "Authorization": f"Bearer {os.environ.get("SHEETY_BEARER_TOKEN")}"
}


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.prices_data = []

    def get_data(self):
        """Returns a list with all the data found into Google Sheets target sheet."""
        response = requests.get(url=SHEETY_GET_ENDPOINT, headers=HEADERS)
        json_data = response.json()

        self.prices_data = json_data["prices"]
        return self.prices_data

    def update_sheet_iata_code(self, iata_code, city_name):
        """Update a specific row from Google Sheets target sheet, with a new iataCode"""
        id_row = [data_row['id'] for data_row in self.prices_data if data_row["city"] == city_name][0]

        update_body = {
            "price": {
                "iataCode": iata_code
            }
        }
        requests.put(url=f"{SHEETY_GET_ENDPOINT}/{id_row}", json=update_body, headers=HEADERS)
