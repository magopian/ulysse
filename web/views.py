from django.template import RequestContext
from django.shortcuts import render_to_response

def show_home(request):
    params = {}
    return render_to_response('web/home.html',params,context_instance=RequestContext(request))