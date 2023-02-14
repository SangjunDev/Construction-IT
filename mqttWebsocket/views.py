from django.shortcuts import render, redirect
import paho.mqtt.client as mqtt
from django.http import JsonResponse
from django.apps import apps
import time
import threading

mqttClient = mqtt.Client(transport='websockets')
mqttClient.username_pw_set("user","1234")
mqttClient.connect("cnditest.kro.kr" ,9001 , 60)

def pub(request):
  return render(request, 'blog/index.html')

def publish(request):

  if request.method =="POST":
      topic = request.POST.get("topic",None)
      Message = request.POST.get("message",None)  
      mqttClient.publish(topic, Message, 1)
  return redirect('/')



