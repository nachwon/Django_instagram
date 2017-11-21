from rest_framework import serializers
from rest_framework.authtoken.models import Token

from member.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'nickname',
            'img_profile',
            'age'
        )


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password1',
            'password2',
            'nickname',
            'img_profile',
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("password is not equal")
        return data

    def create(self, validated_data):
        # User.objects.create_user() 와 동일
        user = User(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        data = {
            'user': ret,
            'token': instance.token,
        }
        return data
