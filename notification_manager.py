from twilio.rest import Client
import os
import smtplib

MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
# This is a random phone number that TWILIO will generate for you
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

# Set personal data for email
MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS")
MY_PASSWORD = os.environ.get("MY_PASSWORD")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message_body):
        """Sends SMS with message composed by FlightData argument data and currency sign for a complete body message"""

        # Send messages with TWILIO
        message = self.client.messages.create(body=message_body,
                                              from_=TWILIO_PHONE_NUMBER,
                                              to=MY_PHONE_NUMBER)
        # Status of message if is in queue to be sent
        print(message.status)

    def send_emails(self, users_data, content_email):
        # For host argument use the specific email provider that you have
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL_ADDRESS, password=MY_PASSWORD)

            for user_data in users_data:
                connection.sendmail(
                    to_addrs=user_data["email"],
                    from_addr=MY_EMAIL_ADDRESS,
                    msg=f"Subject:Flight deal alert!\n\nDear {user_data['firstName']} {user_data['lastName']},\n\n{content_email}".encode('utf-8')
                )
