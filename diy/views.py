from models import DIY_Neighborhood
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point, Polygon

def index(request):
    return render_to_response('diy.html', {})

def create(request):
    message=""
    if request.method == 'POST':
        n = DIY_Neighborhood(name=request.POST['name'], poly=Polygon(fromstr(poly=request.POST['poly'])))
        n.save()
        print request.POST
        message = "This is an XHR POST request"
    return HttpResponse(message)





