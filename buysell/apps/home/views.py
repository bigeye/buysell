from django.core.context_processors import csrf

from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    c = {}
    c.update(csrf(request))
    if request.user:
        c.update({'user': request.user})    # pass value
    return render_to_response("index.html", c)

def register(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("register.html", c)

def write(request):
    c = {}
    c.update(csrf(request))
    if request.user:
        c.update({'user': request.user})    # pass value
    return render_to_response("write.html", c)
