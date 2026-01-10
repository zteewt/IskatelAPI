from django.contrib import admin
from django.urls import path, include
from .views import RegisterView

urlpatterns = [
    path('', include('rest_framework.urls')),   # login/, logout/
    path('register/', RegisterView.as_view(), name='register'),
]