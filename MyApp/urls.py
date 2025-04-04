"""Urls from my app"""

from django.urls import path
from . import views

app_name = 'MyApp'
urlpatterns = [
    path('',views.index, name='index'),
    path('topics/',views.topics, name='topics'),
]
