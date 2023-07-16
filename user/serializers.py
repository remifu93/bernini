from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'date_joined',
        ]


class TokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = self.user.email
        return data