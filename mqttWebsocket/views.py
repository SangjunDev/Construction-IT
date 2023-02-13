from django.shortcuts import render, redirect

import paho.mqtt.client as mqtt

from .forms import PostForm
from django.forms import model_to_dict
from django.http import JsonResponse

def pub(request):
  return render(request, 'blog/index.html')


def publish(request):
  
  mqttClient = mqtt.Client(transport='websockets')
  mqttClient.username_pw_set("user","1234")
  mqttClient.connect("cnditest.kro.kr" ,9001 , 60)
  
  if request.method =="POST":
      topic = request.POST.get("topic",None)
      Message = request.POST.get("message",None)  
        
      mqttClient.publish(topic, Message, 1)
    

  return redirect('/')
