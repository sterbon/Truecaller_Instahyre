from django.apps import AppConfig
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

class ApiConfig(AppConfig):
    name = 'api'
