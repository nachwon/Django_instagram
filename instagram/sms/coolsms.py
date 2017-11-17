from rest_framework.response import Response
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


def send_sms(receiver, message):

    api_key = "NCSGLMHSQ2FTVZUA"
    api_secret = "2ZNM5ZPZR07QHSLHVIFAH3XZR1GAGM2F"
    params = dict()
    params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
    params['to'] = receiver  # Recipients Number '01000000000,01000000001'
    params['from'] = '01029953874'  # Sender number
    params['text'] = message  # Message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        data = {
            "result": "Message have been sent",
            "type": params['type'],
            "sent_from": params['from'],
            "sent_to": receiver,
            "message": message
        }

        if "error_list" in response:
            data = {
                "result": "Failed to send a message"
            }

        return data

    except CoolsmsException as e:
        data = {
            "error": e
        }

        return data
