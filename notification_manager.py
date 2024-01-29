from twilio.rest import Client
from flight_data import FlightData
import os

MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
# This is a random phone number that TWILIO will generate for you
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, flight_data: FlightData, currency_sign):
        """Sends SMS with message composed by FlightData argument data and currency sign for a complete body message"""
        msg_body = (f"Low price alert! Only {currency_sign} {flight_data.price} to fly from "
                    f"{flight_data.from_city}-{flight_data.from_airport_code} to "
                    f"{flight_data.to_city}-{flight_data.to_airport_code}, "
                    f"from {flight_data.departure_date} to {flight_data.arrival_date}.")
        message = self.client.messages.create(body=msg_body,
                                              from_=TWILIO_PHONE_NUMBER,
                                              to=MY_PHONE_NUMBER)
        # Status of message if is in queue to be sent
        print(message.status)
