from twilio.rest import Client
import configparser


class SMSService:

    def __init__(self, config: configparser.ConfigParser):
        self.account_sid = config["SMS"]["account_sid"]
        self.auth_token = config["SMS"]["auth_token"]
        self.twilio_number = config["SMS"]["twilio_number"]
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, recipient_number: str, body: str):
        self.client.messages.create(
            body=body, from_=self.twilio_number, to=recipient_number
        )
        pass
