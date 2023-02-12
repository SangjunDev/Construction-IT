from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

from .models import *

def view_manage(request):
    User = get_user_model()

    current_user = request.user
    if current_user.is_authenticated:
        manages = Manage.objects.filter(user=current_user)
        context = {'manages': manages}

        return render(request, 'blog/index.html', context)
    else:
        return render(request, 'login.html')
