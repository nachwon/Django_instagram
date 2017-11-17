import sys

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

from sms.coolsms import send_sms
from .serializers import SMSSerializer


class SendSMS(APIView):

    def post(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            result = send_sms(**serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


