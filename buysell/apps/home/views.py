from django.core.context_processors import csrf

from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    c = {}
    c.update(csrf(request))
    if request.user:
        c.update({'user': request.user})
    return render_to_response("index.html", c)

