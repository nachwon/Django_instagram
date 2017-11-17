import sys

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

from utils.serializers import SMSSerializer


class SendSMS(APIView):
    api_key = "NCSGLMHSQ2FTVZUA"
    api_secret = "2ZNM5ZPZR07QHSLHVIFAH3XZR1GAGM2F"

    def post(self, request):
        serializer = SMSSerializer(request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        params = dict()
        params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
        params['to'] = '01064626406'  # Recipients Number '01000000000,01000000001'
        params['from'] = '01029953874'  # Sender number
        params['text'] = '이한영 강사님께서 PLAYERUNKNOWN\'S BATTLEGROUNDS 에 접속하셨습니다.'  # Message

        cool = Message(self.api_key, self.api_secret)
        try:
            response = cool.send(params)
            data = {
                "result": "Message have been sent",
                "type": params['type'],
                "sent_from": params['from'],
                "sent_to": params['to'],
                "message": params['text']
            }

            if "error_list" in response:
                data = {
                    "result": "Failed to send a message"
                }

            return Response(data)

        except CoolsmsException as e:
            data = {
                "error": e
            }

            return Response(data)
