from django.contrib import admin
from django.urls import path

from.views import home

app_name = 'user-page'
urlpatterns = [
    path('',home, name='user')
]
