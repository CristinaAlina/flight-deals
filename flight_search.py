import requests
import os
from flight_data import FlightData

HEADERS = {
    "apikey": os.environ.get("TEQUILA_KIWI_API_KEY")
}


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.kiwi_endpoint = "https://api.tequila.kiwi.com"

    def get_iata_code(self, city_name):
        """Returns IATA code of the city received as an argument.
        In case of the IATA code is not found, it will return 'NOT FOUND'."""
        location_endpoint = f"{self.kiwi_endpoint}/locations/query"
        body_query = {
            "term": city_name,
            "locale": "en-US",
            "location_types": "city"
        }
        response = requests.get(url=location_endpoint, params=body_query, headers=HEADERS)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            city_data = response.json()
            if len(city_data["locations"]) == 0:
                return "NOT FOUND"
            else:
                return city_data["locations"][0]["code"]

    def search_flight(self, origin_city_code, destination_city_code, from_date, to_date, currency) -> FlightData:
        """Searches for the cheaper flight to specific location and returns a FlightData type if data was found,
        or None otherwise."""
        search_endpoint = f"{self.kiwi_endpoint}/v2/search"

        body_query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_date.strftime("%d/%m/%Y"),
            "date_to": to_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "curr": currency,
            "adults": 2,
            "one_for_city": 1,
            "max_stopovers": 0
        }
        response = requests.get(url=search_endpoint, params=body_query, headers=HEADERS)
        if response.status_code == 200:
            search_data = response.json()["data"][0]

            flight_data = FlightData(
                price=search_data["price"],
                from_airport_code=search_data["flyFrom"],
                from_city=search_data["cityFrom"],
                to_airport_code=search_data["flyTo"],
                to_city=search_data["cityTo"],
                departure_date=search_data["route"][0]["local_departure"].split("T")[0],
                arrival_date=search_data["route"][1]["local_departure"].split("T")[0]
            )

            return flight_data
        elif response.status_code == 422:
            return None
        else:
            response.raise_for_status()
