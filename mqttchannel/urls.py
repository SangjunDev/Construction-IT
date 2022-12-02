from django.urls import path

from . import views

urlpatterns = [
    path('/mqtt', views.mqtt, name='mqtt'),
]