import json

import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import exceptions, status
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication


class BaseAuthPermissionClass:
    """
    A base class to extend authentication and permission to APIViews.
    """

    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

class Registration(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        name = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phone = request.data.get('phone')

        user = User(
            username=phone,
            password=password,
            email=email
        )

        user.set_password(password)
        user.save()

        user_profile = UserProfile(
            user=user,
            name=name,
            phone=phone
        ).save()

        if user:
            return Response('Account created', status=200)

        else:
            return Response(status=400, content_type="application/json")


class UsersList(APIView, BaseAuthPermissionClass):
    def get(self, request):
        contacts = UserProfile.objects.all()
        serializer = UserSerializer(contacts, many=True)
        return Response(serializer.data)


class SpamList(APIView, BaseAuthPermissionClass):
    
    def get(self, request):
        spamList = UserProfile.objects.all().exclude(spam=False)
        serializer = UserSerializer(spamList, many=True)
        return Response(serializer.data)

    def post(self, request):
        spam_contact = request.data.get('spam')
        user = None
        name = None

        if(User.objects.filter(username=spam_contact)[0]):
            user = User.objects.filter(username=spam_contact)[0]
            name = UserProfile.objects.filter(user=user).values('name')

        spam = UserProfile(
            user=user,
            name=name,
            phone=spam_contact,
            spam=True,
        )
        spam.save()

        if spam:
            return Response('Spam reported', status=200, content_type="application/json")

        else:
            return Response('Some error occured', status=400, content_type="application/json")

class SearchByName(APIView, BaseAuthPermissionClass):

    def get(self, request):
        keyword = request.data.get('keyword')
        exact = UserProfile.objects.filter(name=keyword).values('name','phone','spam')
        likely = UserProfile.objects.filter(name__contains= keyword).values('name','phone','spam').exclude(name=keyword)

        return Response({exact, likely}, status=200, content_type="application/json")

class SearchById(APIView, BaseAuthPermissionClass):
    
    def get(self, request):
        user_id = request.data.get('id')
        user = UserProfile.objects.filter(user=user_id).values()

        return Response(user, status=200, content_type="application/json")
