from rest_framework import serializers
from users.models import CustomUser
from rest_framework.exceptions import ValidationError


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