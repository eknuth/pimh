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
        points=[]
        for point in request.POST['poly'].split(','):
            points.append(fromstr(point))
        points.append(points[0])
        n = DIY_Neighborhood(poly = Polygon(points), name = request.POST['name'], quad='', wiki='')
        n.save()
        message = "This is an XHR POST request"
        return HttpResponse(message)        


#            print lng
            
#        n = DIY_Neighborhood.create_from_String(name=request.POST['name'], 
#                                                poly=Polygon(fromstr(poly=request.POST['poly'])))
        
#        n.save()
#        print request.POST






