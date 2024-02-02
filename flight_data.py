class FlightData:
    # This class is responsible for structuring the flight data.

    def __init__(self, price, from_airport_code, from_city, to_airport_code, to_city, departure_date, arrival_date,
                 stop_overs=0, via_city=""):
        self.price = price
        self.from_airport_code = from_airport_code
        self.from_city = from_city
        self.to_airport_code = to_airport_code
        self.to_city = to_city
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.stop_overs = stop_overs
        self.via_city = via_city
