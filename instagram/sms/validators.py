from rest_framework import serializers


def phone_number(value):
    value = value.replace('-', '')
    if len(value) not in (10, 11):
        raise serializers.ValidationError('wrong number')
    if not value.startswith('0'):
        raise serializers.ValidationError('wrong number')


def sms_length(value):
    encoded_str = value.encode('cp949')
    if len(encoded_str) > 90:
        raise serializers.ValidationError('90byte 까지만 전송 가능함.')
