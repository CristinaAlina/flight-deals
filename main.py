from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime as dt
from datetime import timedelta as td
import re as regex


ORIGIN_CITY_CODE = "LON"
CURRENCY = "USD"
CURRENCY_SIGN = "$"

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# User interaction
print("Welcome to Angela's Flight Club.")
print("We find the best flight deals and email you.")
first_name = input("What is your first name?\n")
last_name = input("What is your last name?\n")

# Make a regular expression for email validation
regex_email = r'\b[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
email = input("What is your email?\n").lower()
while not regex.fullmatch(regex_email, email):
    if email == "exit":
        exit()
    email = input("Invalid email. What is your email?\n").lower()

double_check_email = input("Type your email again.\n").lower()

while email != double_check_email:
    if double_check_email == "exit":
        exit()
    double_check_email = input("Not a match. Type your email again.\n").lower()

print("You're in the club!")

data_manager.add_new_datarow(first_name, last_name, email)

prices_sheet_data = data_manager.get_prices_data()

if len([row_data["iataCode"] for row_data in prices_sheet_data if row_data["iataCode"] == ""]) >= 1:
    for sheet_row in prices_sheet_data:
        if sheet_row["iataCode"] == "":
            sheet_row["iataCode"] = flight_search.get_iata_code(sheet_row["city"])
            data_manager.update_sheet_iata_code(sheet_row["iataCode"], sheet_row["city"])

# We're looking only for direct flights, that leave anytime between tomorrow and in 6 months (6*30 days)
today_date = dt.today()
tomorrow_date = today_date + td(days=1)
after_today_six_months_date = tomorrow_date + td(days=6 * 30)
for data_row in prices_sheet_data:
    if data_row["iataCode"] != "NOT FOUND":
        flight_data = flight_search.search_flight(origin_city_code=ORIGIN_CITY_CODE,
                                                  destination_city_code=data_row["iataCode"],
                                                  from_date=tomorrow_date,
                                                  to_date=after_today_six_months_date,
                                                  currency=CURRENCY)
        if flight_data is not None:
            if flight_data.price < data_row["lowestPrice"]:
                msg_body = (f"Low price alert! Only {flight_data.price} {CURRENCY_SIGN}  to fly from "
                            f"{flight_data.from_city}-{flight_data.from_airport_code} to "
                            f"{flight_data.to_city}-{flight_data.to_airport_code}, "
                            f"from {flight_data.departure_date} to {flight_data.arrival_date}.")
                if flight_data.stop_overs > 0:
                    msg_body += f"\nFlight has {flight_data.stop_overs} stop over, via {flight_data.via_city}."

                # Send email to users
                users_sheet_data = data_manager.get_users_data()
                notification_manager.send_emails(users_sheet_data, msg_body)

                # Send SMS with flight deal
                # notification_manager.send_sms(flight_data, currency_sign=CURRENCY_SIGN)
            else:
                print(f"{flight_data.to_city}: {flight_data.price} {CURRENCY_SIGN}")