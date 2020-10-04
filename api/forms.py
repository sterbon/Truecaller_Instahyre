from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    phone = serializers.CharField(max_length=10)

def get_cleaned_data(self):
    super(CustomRegisterSerializer, self).get_cleaned_data()
    return {
        'username': self.validated_data.get('username', ''),
        'password1': self.validated_data.get('password1', ''),
        'password2': self.validated_data.get('password2', ''),
        'email': self.validated_data.get('email', ''),
        'phone': self.validated_data.get('phone', ''),
    }
    