from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import update_last_login
from django.conf import settings


User = get_user_model()
validate_username = UnicodeUsernameValidator()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = (
            "id",
            #"username",
            "password",
            "gender",
            "nickname",
            "birthdate",
            "email",
            "address",
        )
        read_only_fields = ("id",)

    def validate_email(self, obj):
        try:
            validate_email(obj)
            return obj
        except ValidationError:
            raise serializers.ValidationError('메일 형식이 올바르지 않습니다.')


    def validate_username(self, obj):
        try:
            validate_username(obj)
            return obj
        except ValidationError:
            raise serializers.ValidationError('메일 형식이 올바르지 않습니다.')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()
        return user
    


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        
        if user is None:
            return {
                'email': 'None'
            }

        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)

        return {
            'email': user.email,
            'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }