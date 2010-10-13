from diy.models import DIY_Neighborhood
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point, Polygon

def index(request):
    all_n = DIY_Neighborhood.objects.all()
    print all_n
    return render_to_response('diy.html', {'all_n': all_n})

def edit(request):
    return render_to_response('diy_edit.html', {})

def create(request):
    message=""
    
    if request.method == 'POST':
        points=[]
        for point in request.POST['poly'].split(','):
            points.append(fromstr(point))
        points.append(points[0])
        n = DIY_Neighborhood(poly = Polygon(points), name = request.POST['name'], quad='', wiki='')
        n.save()
        message = "This is an XHR POST request"
        return HttpResponse(message)        

def kml(request):
    all_n = DIY_Neighborhood.objects.all()
    return render_to_response('base.kml', {'all_n': all_n},
            mimetype="application/vnd.google-earth.kml+xml")






