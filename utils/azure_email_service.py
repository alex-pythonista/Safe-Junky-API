from azure.communication.email import EmailClient
from django.conf import settings


def send_email(to, otp):
    email_client = EmailClient.from_connection_string(settings.AZURE_COMMUNICATIONS_CONNECTION_STRING)
    message = {
        "content": {
            "subject": "Please verify OTP",
            "plainText": "Please verify OTP",
            "html": f""" 
                        <html>
                            <body>
                                <p>Hi there,</p>
                                <p>Thanks for registering with us. Please verify your email address by entering the following OTP:)</p>
                                <p><b>{otp}</b></p>
                                <p>Thanks</p>
                        """

        },
        "recipients": {
            "to": [
                {
                    "address": to,
                    "displayName": "Adib"
                }
            ]
        },
        "senderAddress": "adib-the-azure-guy@5c205690-56b0-475b-ac15-b3c59cf37e55.azurecomm.net",
    }
    email_client.begin_send(message)