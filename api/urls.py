from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework_simplejwt import views as jwt_views

from api import views

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/jwt', jwt_views.TokenObtainPairView.as_view(), name='obtain-jwt'),
    path('auth/jwt/refresh', jwt_views.TokenRefreshView.as_view(), name='refresh-jwt'),
    path('signup/', views.Registration.as_view()),
    path('users/', views.UsersList.as_view()),
    path('add-spam/', views.SpamList.as_view()),
    path('get-spam/', views.SpamList.as_view()),
    path('search-name/', views.SearchByName.as_view()),
    path('search-id/', views.SearchById.as_view())
]
