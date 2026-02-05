from rest_framework import serializers
from users.models import CustomUser
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class OAuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    


class UserCreateSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email

        return ValidationError("Email already exists!")
    

class ConfirmUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, email):
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return email