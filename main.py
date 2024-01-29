from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime as dt
from datetime import timedelta as td


ORIGIN_CITY_CODE = "LON"
CURRENCY = "GBP"
CURRENCY_SIGN = "£"

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_data()

if len([row_data["iataCode"] for row_data in sheet_data if row_data["iataCode"] == ""]) >= 1:
    for sheet_row in sheet_data:
        if sheet_row["iataCode"] == "":
            sheet_row["iataCode"] = flight_search.get_iata_code(sheet_row["city"])
            data_manager.update_sheet_iata_code(sheet_row["iataCode"], sheet_row["city"])

# We're looking only for direct flights, that leave anytime between tomorrow and in 6 months (6*30 days)
today_date = dt.today()
tomorrow_date = today_date + td(days=1)
after_today_six_months_date = tomorrow_date + td(days=6 * 30)

for data_row in sheet_data:
    if data_row["iataCode"] != "NOT FOUND":
        flight_data = flight_search.search_flight(ORIGIN_CITY_CODE,
                                                  data_row["iataCode"],
                                                  tomorrow_date,
                                                  after_today_six_months_date,
                                                  CURRENCY)
        if flight_data is not None:
            if flight_data.price < data_row["lowestPrice"]:
                print(f"{flight_data.to_city}: {CURRENCY_SIGN}{flight_data.price}")
                # Send SMS with flight deal
                notification_manager.send_sms(flight_data, currency_sign=CURRENCY_SIGN)