
from twilio.rest import TwilioRestClient
import os

def text_alert(phone):

    # Twilio Account Information
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    twilio_number = os.environ["TWILIO_NUMBER"]

    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(body="You have a note waiting to be read! Go and check it out on WOURDS",
                                    from_=twilio_number,
                                    to=phone)
