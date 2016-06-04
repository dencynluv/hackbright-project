# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
import os

def text_alert():

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]

    twilio_number = "+13125481634"
    msg = "You have a note waiting to be read."

    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(body=msg,
                                    from_=twilio_number,
                                    to="+13126139545")
