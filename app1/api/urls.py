
from django.contrib import admin
from django.urls import path, include
from app1.views import loginAPI, signupAPI,protected_view
urlpatterns = [
    path('auth/login/', loginAPI),
    path('auth/signup/', signupAPI),
    path('auth/test/', protected_view),
]
