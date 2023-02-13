from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_manage, name="control_data"),
]