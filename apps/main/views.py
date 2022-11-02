from django.conf import settings
from django.shortcuts import render
from django.conf import settings

def media_admin(request):
    return {'media':settings.MEDIA_URL}

def index(request):
    return render(request,"main/index.html")