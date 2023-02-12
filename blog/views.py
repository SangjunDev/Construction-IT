from django.shortcuts import render
from users.models import User
from users.decorators import login_message_requred

# Create your views here.

@login_message_requred
def index(request):
  return render(
    request, 
    'blog/index.html'
  )



  