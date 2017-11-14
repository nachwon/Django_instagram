from rest_framework import serializers
from rest_framework.authtoken.models import Token

from member.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'nickname',
            'img_profile',
            'age'
        )


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password1',
            'password2',
            'nickname',
            'img_profile',
            'token',
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

    def get_token(self, obj):
        return Token.objects.create(user=obj).key
