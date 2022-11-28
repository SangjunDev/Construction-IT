from django.shortcuts import render
from django.http import HttpResponse
from . import mqttWebsocket as mqtt

def mqttTest(request):
  return render(request, 'access/about.html')

def led_on(request):
  pass

def led_off(request):
  pass

def led_detecte(request):
  pass

